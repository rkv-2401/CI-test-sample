"""XDIST HAZARD 4 (with test_cache_hazard_a): clears the shared cache file."""
import time
import unittest

from stocks.store import cache_clear, cache_get


class CacheClear(unittest.TestCase):
    def test_clear_empties_cache(self):
        for _ in range(20):          # keep clearing for a while, as a slow test's teardown might
            cache_clear()
            time.sleep(0.05)
        self.assertIsNone(cache_get("ACME"))
