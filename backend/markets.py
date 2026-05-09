"""
Live market data:
  - Index data (SPX, NDX, DJI) via Yahoo Finance REST API
  - US top movers via Futu OpenD (falls back to static snapshot if OpenD not running)
"""
import logging
import requests
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

_cache: dict = {}
_cache_time: Optional[datetime] = None
CACHE_TTL = timedelta(seconds=55)

YAHOO_INDICES = {
    "SPX": {"ticker": "^GSPC", "name": "S&P 500"},
    "NDX": {"ticker": "^NDX",  "name": "Nasdaq 100"},
    "DJI": {"ticker": "^DJI",  "name": "Dow Jones"},
}

_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

YAHOO_MOVERS = [
    {"ticker": "AAPL",  "yahoo": "AAPL",  "name": "Apple"},
    {"ticker": "MSFT",  "yahoo": "MSFT",  "name": "Microsoft"},
    {"ticker": "NVDA",  "yahoo": "NVDA",  "name": "NVIDIA"},
    {"ticker": "AMZN",  "yahoo": "AMZN",  "name": "Amazon"},
    {"ticker": "GOOGL", "yahoo": "GOOGL", "name": "Alphabet"},
    {"ticker": "META",  "yahoo": "META",  "name": "Meta Platforms"},
    {"ticker": "TSLA",  "yahoo": "TSLA",  "name": "Tesla"},
    {"ticker": "LLY",   "yahoo": "LLY",   "name": "Eli Lilly"},
    {"ticker": "AVGO",  "yahoo": "AVGO",  "name": "Broadcom"},
    {"ticker": "BRK.B", "yahoo": "BRK-B", "name": "Berkshire Hathaway B"},
]


def _fetch_yahoo_quote(ticker: str) -> dict:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=2d"
    r = requests.get(url, headers=_YAHOO_HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    meta = data["chart"]["result"][0]["meta"]
    price = float(meta["regularMarketPrice"])
    prev  = float(meta.get("chartPreviousClose") or meta.get("previousClose") or price)
    chg   = round(price - prev, 4)
    chg_pct = round((chg / prev * 100) if prev else 0.0, 2)
    return {"price": price, "change": chg, "change_pct": chg_pct}


def _fetch_indices_yahoo() -> list:
    indices = []
    for sym, meta in YAHOO_INDICES.items():
        try:
            q = _fetch_yahoo_quote(meta["ticker"])
            indices.append({
                "symbol": sym,
                "name": meta["name"],
                **q,
            })
        except Exception as exc:
            logger.warning("Yahoo Finance failed for %s: %s", sym, exc)
            indices.append({"symbol": sym, "name": meta["name"], "price": 0.0, "change": 0.0, "change_pct": 0.0})
    return indices


def _fetch_movers_yahoo() -> list:
    movers = []
    for m in YAHOO_MOVERS:
        try:
            q = _fetch_yahoo_quote(m["yahoo"])
            movers.append({
                "ticker": m["ticker"],
                "name": m["name"],
                "price": q["price"],
                "change_pct": q["change_pct"],
                "volume": 0,
            })
        except Exception as exc:
            logger.warning("Yahoo movers failed for %s: %s", m["ticker"], exc)
    movers.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
    return movers


def get_market_data() -> dict:
    global _cache, _cache_time
    if _cache_time and datetime.utcnow() - _cache_time < CACHE_TTL:
        return _cache

    indices = _fetch_indices_yahoo()

    try:
        movers = _fetch_movers_yahoo()
        source = "yahoo"
    except Exception as exc:
        logger.warning("Yahoo movers failed (%s)", exc)
        movers = []
        source = "unavailable"

    result = {
        "indices": indices,
        "movers": movers,
        "source": source,
        "as_of": datetime.utcnow().isoformat(),
    }
    _cache = result
    _cache_time = datetime.utcnow()
    return _cache
