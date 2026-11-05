"""
Movies Treasure Pro
https://github.com/Rabbani78689/Movies-Treasure-Pro
Author: Rabbani
License: MIT
"""

from fastapi import APIRouter
from . import user, providers, home, catalog, search, stream, diagnostics

router = APIRouter()
for _r in (
    user.router,
    providers.router,
    home.router,
    catalog.router,
    search.router,
    stream.router,
    diagnostics.router,
):
    router.include_router(_r)
