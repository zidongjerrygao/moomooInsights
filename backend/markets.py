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

US_MOVERS_TICKERS = [
    "US.AAPL",
    "US.MSFT",
    "US.NVDA",
    "US.AMZN",
    "US.GOOGL",
    "US.META",
    "US.TSLA",
    "US.LLY",
    "US.AVGO",
    "US.BRK.B",
]

_FALLBACK_MOVERS = [
    {"ticker": "AAPL",  "name": "Apple",                "price": 293.32, "change_pct": 2.05,  "volume": 54200000},
    {"ticker": "MSFT",  "name": "Microsoft",            "price": 415.12, "change_pct": -1.34, "volume": 21300000},
    {"ticker": "NVDA",  "name": "NVIDIA",               "price": 215.20, "change_pct": 1.75,  "volume": 89600000},
    {"ticker": "AMZN",  "name": "Amazon",               "price": 272.68, "change_pct": 0.56,  "volume": 31400000},
    {"ticker": "GOOGL", "name": "Alphabet",             "price": 400.80, "change_pct": 0.71,  "volume": 18700000},
    {"ticker": "META",  "name": "Meta Platforms",       "price": 609.63, "change_pct": -1.16, "volume": 12900000},
    {"ticker": "TSLA",  "name": "Tesla",                "price": 428.35, "change_pct": 4.02,  "volume": 67800000},
    {"ticker": "LLY",   "name": "Eli Lilly",            "price": 948.45, "change_pct": -2.72, "volume": 3100000},
    {"ticker": "AVGO",  "name": "Broadcom",             "price": 430.00, "change_pct": 4.23,  "volume": 9400000},
    {"ticker": "BRK.B", "name": "Berkshire Hathaway B", "price": 475.94, "change_pct": 0.18,  "volume": 4600000},
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


def _fetch_movers_futu() -> list:
    from futu import OpenQuoteContext, RET_OK
    ctx = OpenQuoteContext(host="127.0.0.1", port=11111)
    try:
        ret, data = ctx.get_market_snapshot(US_MOVERS_TICKERS)
        if ret != RET_OK or data.empty:
            return list(_FALLBACK_MOVERS)
        movers = []
        for _, r in data.iterrows():
            price = float(r["last_price"])
            prev  = float(r.get("prev_close_price", price) or price)
            chg_pct = round(((price - prev) / prev * 100) if prev else 0.0, 2)
            movers.append({
                "ticker": r["code"].split(".")[-1],
                "name": str(r["name"]),
                "price": price,
                "change_pct": chg_pct,
                "volume": int(r.get("volume", 0)),
            })
        movers.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
        return movers[:10]
    finally:
        ctx.close()


def get_market_data() -> dict:
    global _cache, _cache_time
    if _cache_time and datetime.utcnow() - _cache_time < CACHE_TTL:
        return _cache

    indices = _fetch_indices_yahoo()

    try:
        movers = _fetch_movers_futu()
        source = "futu"
    except Exception as exc:
        logger.warning("Futu OpenD unavailable (%s) — using fallback movers", exc)
        movers = list(_FALLBACK_MOVERS)
        source = "fallback"

    result = {
        "indices": indices,
        "movers": movers,
        "source": source,
        "as_of": datetime.utcnow().isoformat(),
    }
    _cache = result
    _cache_time = datetime.utcnow()
    return _cache
