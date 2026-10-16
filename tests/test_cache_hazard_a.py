"""XDIST HAZARD 4 (with test_cache_hazard_b): two modules share one fixed file.

This module fills out/price_cache.json, does some work, then expects its entry
back. test_cache_hazard_b clears the same file. Sequentially, a finishes
before b starts. Under `pytest -n 4` they can run at the same moment on
different workers, and b deletes the cache between a's write and a's read.
It fails only sometimes: a flaky test, the hardest kind to trust.
"""
import random
import unittest

from stocks.prices import simulate_prices
from stocks.store import cache_get, cache_put
from stocks.strategy import backtest


class CacheRoundTrip(unittest.TestCase):
    def test_put_then_get(self):
        prices = simulate_prices(100, 200_000, 0.0, 0.01, random.Random(3))
        cache_put("ACME", prices[:100])
        backtest(prices, short=10, long=50)  # time passes; b may run now
        self.assertEqual(cache_get("ACME"), prices[:100])
