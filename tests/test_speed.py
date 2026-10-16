"""Clean but slow: stands in for the simulation-backed modules.

Each test backtests a long simulated history. They share nothing, so xdist
can spread them across workers and the wall-clock time drops.
"""
import random
import unittest

from stocks.prices import simulate_prices
from stocks.strategy import backtest

DAYS = 300_000


class LongBacktests(unittest.TestCase):
    def run_one(self, seed):
        prices = simulate_prices(100, DAYS, 0.0002, 0.015, random.Random(seed))
        result = backtest(prices, short=10, long=50)
        self.assertGreater(result["final_value"], 0)

    def test_seed_1(self):
        self.run_one(1)

    def test_seed_2(self):
        self.run_one(2)

    def test_seed_3(self):
        self.run_one(3)

    def test_seed_4(self):
        self.run_one(4)
