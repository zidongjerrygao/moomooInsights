"""
Live market data:
  - Primary: Futu OpenD (localhost:11111) — indices + top movers with real-time volume
  - Fallback: Yahoo Finance REST API when OpenD is not running
"""
import logging
import socket
import requests
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

_cache: dict = {}
_cache_time: Optional[datetime] = None
CACHE_TTL = timedelta(seconds=55)

FUTU_HOST = "127.0.0.1"
FUTU_PORT = 11111

YAHOO_INDICES = {
    "SPX": {"ticker": "^GSPC", "name": "S&P 500"},
    "NDX": {"ticker": "^NDX",  "name": "Nasdaq 100"},
    "DJI": {"ticker": "^DJI",  "name": "Dow Jones"},
}

FUTU_INDICES = [
    {"code": "US.SPX", "symbol": "SPX", "name": "S&P 500"},
    {"code": "US.NDX", "symbol": "NDX", "name": "Nasdaq 100"},
    {"code": "US.DJI", "symbol": "DJI", "name": "Dow Jones"},
]

_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

MOVERS = [
    {"ticker": "AAPL",  "futu": "US.AAPL",  "yahoo": "AAPL",  "name": "Apple"},
    {"ticker": "MSFT",  "futu": "US.MSFT",  "yahoo": "MSFT",  "name": "Microsoft"},
    {"ticker": "NVDA",  "futu": "US.NVDA",  "yahoo": "NVDA",  "name": "NVIDIA"},
    {"ticker": "AMZN",  "futu": "US.AMZN",  "yahoo": "AMZN",  "name": "Amazon"},
    {"ticker": "GOOGL", "futu": "US.GOOGL", "yahoo": "GOOGL", "name": "Alphabet"},
    {"ticker": "META",  "futu": "US.META",  "yahoo": "META",  "name": "Meta Platforms"},
    {"ticker": "TSLA",  "futu": "US.TSLA",  "yahoo": "TSLA",  "name": "Tesla"},
    {"ticker": "LLY",   "futu": "US.LLY",   "yahoo": "LLY",   "name": "Eli Lilly"},
    {"ticker": "AVGO",  "futu": "US.AVGO",  "yahoo": "AVGO",  "name": "Broadcom"},
    {"ticker": "BRK.B", "futu": "US.BRK-B", "yahoo": "BRK-B", "name": "Berkshire Hathaway B"},
]

# Keep legacy alias used elsewhere
YAHOO_MOVERS = MOVERS


# ── OpenD helpers ─────────────────────────────────────────────────────────────

def _is_opend_running(timeout: float = 1.0) -> bool:
    """TCP probe — avoids SDK hang when OpenD is not running."""
    try:
        with socket.create_connection((FUTU_HOST, FUTU_PORT), timeout=timeout):
            return True
    except OSError:
        return False


def _futu_snapshot(codes: list):
    """Return a pandas DataFrame from OpenD get_market_snapshot. Raises on error."""
    import futu
    ctx = futu.OpenQuoteContext(host=FUTU_HOST, port=FUTU_PORT)
    try:
        ret, data = ctx.get_market_snapshot(codes)
        if ret != futu.RET_OK:
            raise RuntimeError(f"OpenD: {data}")
        return data
    finally:
        ctx.close()


def _fetch_indices_futu() -> list:
    codes = [f["code"] for f in FUTU_INDICES]
    df = _futu_snapshot(codes)
    code_map = {f["code"]: f for f in FUTU_INDICES}
    indices = []
    for _, row in df.iterrows():
        meta = code_map.get(row["code"])
        if not meta:
            continue
        price = float(row["last_price"])
        prev  = float(row["prev_close_price"])
        chg   = round(price - prev, 4)
        chg_pct = round(float(row["change_rate"]), 2)
        indices.append({
            "symbol": meta["symbol"],
            "name": meta["name"],
            "price": price,
            "change": chg,
            "change_pct": chg_pct,
        })
    return indices


def _fetch_movers_futu() -> list:
    codes = [m["futu"] for m in MOVERS]
    df = _futu_snapshot(codes)
    code_map = {m["futu"]: m for m in MOVERS}
    movers = []
    for _, row in df.iterrows():
        meta = code_map.get(row["code"])
        if not meta:
            continue
        movers.append({
            "ticker": meta["ticker"],
            "name": meta["name"],
            "price": float(row["last_price"]),
            "change_pct": round(float(row["change_rate"]), 2),
            "volume": int(row.get("volume", 0) or 0),
        })
    movers.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
    return movers


# ── Yahoo Finance helpers ─────────────────────────────────────────────────────

def _fetch_yahoo_quote(ticker: str) -> dict:
    last_exc = None
    for host in ("query1", "query2"):
        try:
            url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=2d"
            r = requests.get(url, headers=_YAHOO_HEADERS, timeout=10)
            r.raise_for_status()
            data = r.json()
            result = data["chart"]["result"][0]
            meta = result["meta"]
            price = float(meta["regularMarketPrice"])
            # Use closes[0] from the 2-day window: that's the previous session's final close.
            # chartPreviousClose is the close before the window starts — one day too far back.
            closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            closes = [c for c in closes if c is not None]
            if len(closes) >= 2:
                prev = float(closes[0])
            else:
                prev = float(meta.get("chartPreviousClose") or meta.get("previousClose") or price)
            chg   = round(price - prev, 4)
            chg_pct = round((chg / prev * 100) if prev else 0.0, 2)
            return {"price": price, "change": chg, "change_pct": chg_pct}
        except Exception as exc:
            last_exc = exc
    raise last_exc


def _fetch_indices_yahoo() -> list:
    indices = []
    for sym, meta in YAHOO_INDICES.items():
        try:
            q = _fetch_yahoo_quote(meta["ticker"])
            indices.append({"symbol": sym, "name": meta["name"], **q})
        except Exception as exc:
            logger.warning("Yahoo Finance failed for %s: %s", sym, exc)
            indices.append({"symbol": sym, "name": meta["name"],
                            "price": 0.0, "change": 0.0, "change_pct": 0.0})
    return indices


def _fetch_movers_yahoo() -> list:
    movers = []
    for m in MOVERS:
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


# ── Single-ticker on-demand quote ────────────────────────────────────────────

_quote_cache: dict[str, tuple[datetime, dict]] = {}


def fetch_quote(ticker: str) -> Optional[dict]:
    """Fetch a live quote for any ticker symbol. Returns None on failure."""
    ticker = ticker.upper().strip()
    now = datetime.utcnow()
    if ticker in _quote_cache:
        cached_at, cached_val = _quote_cache[ticker]
        if now - cached_at < CACHE_TTL:
            return cached_val
    try:
        # Map common index names to Yahoo symbols
        yahoo_sym = {"SPX": "^GSPC", "NDX": "^NDX", "DJI": "^DJI",
                     "VIX": "^VIX", "RUT": "^RUT"}.get(ticker, ticker)
        q = _fetch_yahoo_quote(yahoo_sym)
        # Try to get the company name from Yahoo metadata
        name = ""
        for host in ("query1", "query2"):
            try:
                import requests as _req
                url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{yahoo_sym}?interval=1d&range=2d"
                r = _req.get(url, headers=_YAHOO_HEADERS, timeout=8)
                r.raise_for_status()
                meta = r.json()["chart"]["result"][0]["meta"]
                name = meta.get("shortName") or meta.get("longName") or ""
                break
            except Exception:
                pass
        result = {"ticker": ticker, "name": name, **q}
        _quote_cache[ticker] = (now, result)
        return result
    except Exception as exc:
        logger.debug("fetch_quote failed for %s: %s", ticker, exc)
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def get_market_data() -> dict:
    global _cache, _cache_time
    if _cache_time and datetime.utcnow() - _cache_time < CACHE_TTL:
        return _cache

    indices = _fetch_indices_yahoo()

    try:
        movers = _fetch_movers_yahoo()
    except Exception as exc:
        logger.warning("Yahoo movers failed (%s)", exc)
        movers = []

    result = {
        "indices": indices,
        "movers": movers,
        "source": "yahoo",
        "as_of": datetime.utcnow().isoformat(),
    }
    _cache = result
    _cache_time = datetime.utcnow()
    return _cache
