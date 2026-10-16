"""Files on disk: a price cache and a backtest report.

Both default to fixed paths under out/, the way Ben's tests read plants from
out/. Every function also takes a path, so a test can point it somewhere private.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
CACHE = OUT / "price_cache.json"
REPORT = OUT / "report.json"


def _read(path):
    return json.loads(path.read_text()) if path.exists() else {}


def cache_put(symbol, prices, path=CACHE):
    data = _read(path)
    data[symbol] = prices
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def cache_get(symbol, path=CACHE):
    return _read(path).get(symbol)


def cache_clear(path=CACHE):
    path.unlink(missing_ok=True)


def write_report(result, path=REPORT):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2))


def read_report(path=REPORT):
    return json.loads(path.read_text())
