"""Clean: pure functions, a private temp file, a local random generator."""
import random
import tempfile
import unittest
from datetime import date
from pathlib import Path

from stocks.prices import daily_returns, load_prices, moving_average, simulate_prices


class Indicators(unittest.TestCase):
    def test_moving_average(self):
        self.assertEqual(moving_average([1, 2, 3, 4, 5], 3), [None, None, 2, 3, 4])

    def test_moving_average_rejects_zero_window(self):
        with self.assertRaises(ValueError):
            moving_average([1, 2], 0)

    def test_daily_returns(self):
        for got, want in zip(daily_returns([100, 110, 99]), [0.10, -0.10]):
            self.assertAlmostEqual(got, want)


class Loading(unittest.TestCase):
    def test_load_sorts_by_date(self):
        with tempfile.TemporaryDirectory() as d:
            csv = Path(d) / "acme.csv"
            csv.write_text("date,close\n2026-01-02,11\n2026-01-01,10\n")
            self.assertEqual(load_prices(csv), [(date(2026, 1, 1), 10.0), (date(2026, 1, 2), 11.0)])


class Simulating(unittest.TestCase):
    def test_same_seed_same_path(self):
        a = simulate_prices(100, 50, 0.0005, 0.02, random.Random(1))
        b = simulate_prices(100, 50, 0.0005, 0.02, random.Random(1))
        self.assertEqual(a, b)

    def test_prices_stay_positive(self):
        path = simulate_prices(100, 1000, -0.01, 0.2, random.Random(2))
        self.assertTrue(all(p > 0 for p in path))
