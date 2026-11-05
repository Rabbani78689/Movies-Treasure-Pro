"""
Movies Treasure API Pro
https://github.com/Rabbani78689/Movies-Treasure-Pro
Author: Rabbani
License: MIT
"""

import os
from env_loader import load_environment

load_environment()

API_VERSION = "2.9.1"
APP_NAME = os.environ.get("APP_NAME", "Movies Treasure API Pro")
APP_SHORT_NAME = os.environ.get("APP_SHORT_NAME", "Movies Treasure")
APP_TAGLINE = os.environ.get("APP_TAGLINE", "Pure Streaming API Architecture")
DEVELOPER_NAME = os.environ.get("DEVELOPER_NAME", "Rabbani")
DEVELOPER_URL = os.environ.get("DEVELOPER_URL", "https://github.com/Rabbani78689")
PROJECT_URL = os.environ.get("PROJECT_URL", "https://github.com/Rabbani78689/Movies-Treasure-Pro")
ENABLE_ADS = os.environ.get("ENABLE_ADS", "false").strip().lower() in {"1", "true", "yes", "on"}
ADS_PROVIDER = os.environ.get("ADS_PROVIDER", "none")
ADS_CONFIG = os.environ.get("ADS_CONFIG", "")
UPDATE_CHECK_URL = os.environ.get("UPDATE_CHECK_URL", f"{PROJECT_URL}/releases/latest")
FORCE_UPDATE = os.environ.get("FORCE_UPDATE", "false").strip().lower() in {"1", "true", "yes", "on"}
MINIMUM_APP_VERSION = os.environ.get("MINIMUM_APP_VERSION", API_VERSION)

PORT = int(os.environ.get("PORT", "8000"))
BIND_HOST = os.environ.get("MOVIEBOX_BIND_HOST", "127.0.0.1")
REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", "25"))
DOMAIN_TTL = int(os.environ.get("DOMAIN_TTL", "300"))
CORS_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.environ.get("CORS_ORIGINS", "").split(",")
    if origin.strip() and origin.strip() != "*"
]

TAB_MOVIES = int(os.environ.get("TAB_MOVIES", "2"))
TAB_TV = int(os.environ.get("TAB_TV", "5"))
TAB_ANIMATION = int(os.environ.get("TAB_ANIMATION", "8"))

CATALOG_DB = os.environ.get("CATALOG_DB", "catalog.db")
CATALOG_REFRESH_INTERVAL = int(os.environ.get("CATALOG_REFRESH_INTERVAL", "21600"))
CATALOG_KEYWORDS = list("abcdefghijklmnopqrstuvwxyz0123456789")
CATALOG_MAX_PAGES_PER_KEYWORD = int(os.environ.get("CATALOG_MAX_PAGES_PER_KEYWORD", "50"))
ENRICH_RATE_LIMIT = float(os.environ.get("ENRICH_RATE_LIMIT", "0.2"))
ENRICH_BATCH_SIZE = int(os.environ.get("ENRICH_BATCH_SIZE", "20"))

DEFAULT_HOST = os.environ.get("MOVIEBOX_HOST", "moviebox.ph")
KNOWN_HOSTS = [
    h.strip() for h in os.environ.get(
        "MOVIEBOX_HOSTS",
        "moviebox.ph,movie-box.co,movieboxonline.net,movieboxhd.net,123moviesfree.club,sflix.film,netnaija.film",
    ).split(",") if h.strip()
]

PROVIDER_PROBE_INTERVAL = int(os.environ.get("PROVIDER_PROBE_INTERVAL", "60"))
PROVIDER_PROBE_TIMEOUT = float(os.environ.get("PROVIDER_PROBE_TIMEOUT", "8"))
CIRCUIT_BREAKER_THRESHOLD = int(os.environ.get("CIRCUIT_BREAKER_THRESHOLD", "3"))
CIRCUIT_BREAKER_SECONDS = int(os.environ.get("CIRCUIT_BREAKER_SECONDS", "60"))
RETRY_BACKOFF = float(os.environ.get("RETRY_BACKOFF", "0.5"))

API_BASE = "https://h5-api.aoneroom.com/wefeed-h5api-bff"
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Referer": "https://moviebox.ph/",
    "Origin": "https://moviebox.ph",
    "X-Client-Info": '{"timezone":"Asia/Dhaka"}',
    "X-Request-Lang": "en",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
}

PLAYER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "X-Client-Info": '{"timezone":"Asia/Dhaka"}',
    "X-Source": "",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

# Substring keywords used to classify home sections into movie / tv / anime
# buckets. Substring matching (not exact) so this survives geo-shifted home
# feeds — Singapore says "Popular Movie", Mumbai says "Cinema", both match.
CATALOG_SECTIONS = {
    "movies": ["movie", "cinema", "nollywood", "bollywood", "hollywood", "south indian"],
    "tv-series": ["series", "tv", "show", "drama"],
    "animation": ["anime", "animation"],
}

TAB_PAYLOAD_VARIANTS = {
    "baseline":       {"filter": {"sort": "RECOMMEND", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL"}},
    "no_filter":      None,
    "empty_filter":   {"filter": {}},
    "sort_only":      {"filter": {"sort": "RECOMMEND"}},
    "sort_newest":    {"filter": {"sort": "NEWEST", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL"}},
    "sort_hot":       {"filter": {"sort": "HOT", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL"}},
    "sort_rating":    {"filter": {"sort": "RATING", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL"}},
    "type_movie":     {"filter": {"sort": "RECOMMEND", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL", "type": "MOVIE"}},
    "type_series":    {"filter": {"sort": "RECOMMEND", "genre": "ALL", "country": "ALL", "year": "ALL", "language": "ALL", "type": "TV_SERIES"}},
}
