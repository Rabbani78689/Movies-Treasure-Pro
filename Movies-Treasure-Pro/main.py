"""
Movies Treasure API Pro
https://github.com/Rabbani78689/Movies-Treasure-Pro
Author: Rabbani
License: MIT
"""

import os
import sqlite3
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import state
import storage
import providers
import catalog_worker
from config import (
    API_VERSION, PORT, BIND_HOST, CORS_ORIGINS, REQUEST_TIMEOUT, CATALOG_DB, STATIC_DIR,
    APP_NAME, APP_SHORT_NAME, APP_TAGLINE, DEVELOPER_NAME, DEVELOPER_URL,
    PROJECT_URL, ENABLE_ADS, ADS_PROVIDER, ADS_CONFIG, UPDATE_CHECK_URL,
    FORCE_UPDATE, MINIMUM_APP_VERSION,
)
from dashboard import DASHBOARD_HTML
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.client = httpx.AsyncClient(
        timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=10.0),
        limits=httpx.Limits(
            max_connections=50,
            max_keepalive_connections=20,
            keepalive_expiry=30.0,
        ),
        follow_redirects=True,
    )
    state.write_conn = sqlite3.connect(CATALOG_DB, check_same_thread=False)
    state.write_conn.execute("PRAGMA journal_mode=WAL")
    state.write_conn.execute("PRAGMA synchronous=NORMAL")
    storage.init_schema()

    # Refuse to start on a corrupt DB — otherwise every write fails silently
    # with "database disk image is malformed" while reads still succeed,
    # which is very confusing to debug. Better to fail fast and loud.
    try:
        result = state.write_conn.execute("PRAGMA integrity_check").fetchone()
        if result and result[0] != "ok":
            print(f"FATAL: {CATALOG_DB} is corrupt ({result[0]})")
            print(f"Fix: rm -f {CATALOG_DB} {CATALOG_DB}-wal {CATALOG_DB}-shm, then restart")
            raise SystemExit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"integrity check skipped: {e}")

    state.background_task = asyncio.create_task(catalog_worker.maintenance_loop())
    state.probe_task = asyncio.create_task(providers.probe_loop())
    try:
        yield
    finally:
        for t in (state.background_task, state.probe_task):
            if t is not None:
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass
        if state.client is not None:
            await state.client.aclose()
            state.client = None
        if state.write_conn is not None:
            state.write_conn.close()
            state.write_conn = None


app = FastAPI(
    title=APP_NAME,
    description=f"{APP_NAME} — {PROJECT_URL} | Full Pure REST API for streaming workflows and self-hosted frontend",
    version=API_VERSION,
    contact={
        "name": DEVELOPER_NAME,
        "url": DEVELOPER_URL,
    },
    license_info={
        "name": "MIT",
        "url": f"{PROJECT_URL}/blob/main/LICENSE",
    },
    lifespan=lifespan,
)


@app.middleware("http")
async def reject_cross_origin_mutations(request: Request, call_next):
    # The app has no login cookie to provide CSRF protection. Reject browser
    # form/fetch mutations from untrusted origins while allowing native clients
    # that do not send Origin and explicitly configured web clients.
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        origin = request.headers.get("origin")
        if origin:
            scheme = request.headers.get("x-forwarded-proto", request.url.scheme).split(",")[0].strip()
            same_origin = f"{scheme}://{request.headers.get('host', request.url.netloc)}"
            if origin.rstrip("/") not in {same_origin.rstrip("/"), *CORS_ORIGINS}:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Cross-origin mutations are not allowed"},
                )
    return await call_next(request)


if CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )

app.include_router(router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/manifest.json")
async def manifest():
    path = os.path.join(STATIC_DIR, "manifest.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("__APP_NAME__", APP_NAME)
        content = content.replace("__APP_SHORT_NAME__", APP_SHORT_NAME)
        content = content.replace("__APP_DESCRIPTION__", f"{APP_NAME} — {PROJECT_URL}")
        return Response(content=content, media_type="application/manifest+json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="manifest.json not found")


@app.get("/config")
async def app_config():
    return {
        "app_name": APP_NAME,
        "app_short_name": APP_SHORT_NAME,
        "tagline": APP_TAGLINE,
        "developer_name": DEVELOPER_NAME,
        "developer_url": DEVELOPER_URL,
        "project_url": PROJECT_URL,
        "version": API_VERSION,
        "minimum_app_version": MINIMUM_APP_VERSION,
        "force_update": FORCE_UPDATE,
        "update_check_url": UPDATE_CHECK_URL,
        "ads_enabled": ENABLE_ADS,
        "ads_provider": ADS_PROVIDER,
        "ads_config": ADS_CONFIG,
    }


@app.get("/sw.js")
async def service_worker():
    path = os.path.join(STATIC_DIR, "sw.js")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return Response(
                content=f.read(),
                media_type="application/javascript",
                headers={"Service-Worker-Allowed": "/"},
            )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="sw.js not found")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/app", response_class=HTMLResponse)
async def frontend_app():
    path = os.path.join(STATIC_DIR, "app.html")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("__APP_NAME__", APP_NAME)
        content = content.replace("__APP_SHORT_NAME__", APP_SHORT_NAME)
        content = content.replace("__APP_TAGLINE__", APP_TAGLINE)
        content = content.replace("__DEVELOPER_NAME__", DEVELOPER_NAME)
        content = content.replace("__DEVELOPER_URL__", DEVELOPER_URL)
        content = content.replace("__PROJECT_URL__", PROJECT_URL)
        return HTMLResponse(content)
    except FileNotFoundError:
        return HTMLResponse("<h1>app.html not found in static/</h1>", status_code=404)


if __name__ == "__main__":
    import uvicorn
    reload_flag = os.environ.get("RELOAD", "0") == "1"
    uvicorn.run("main:app", host=BIND_HOST, port=PORT, reload=reload_flag)
