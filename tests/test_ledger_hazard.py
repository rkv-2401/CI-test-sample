"""XDIST HAZARD 2: tests share one object built in setUpClass, and each builds on the last.

Sequentially: buy, then sell half, then check the value. Under `pytest -n 4`
(the default --dist load), the methods are sent to different workers. Each
worker runs setUpClass for itself and gets a fresh, empty portfolio, so
test_2 has nothing to sell. `--dist loadscope` keeps a class on one worker
and hides the problem; it doesn't fix it.
"""
import unittest

from stocks.portfolio import Portfolio


class Ledger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = Portfolio(10_000)

    def test_1_buy(self):
        self.p.buy("ACME", 100, 50)
        self.assertEqual(self.p.shares("ACME"), 100)

    def test_2_sell_half(self):
        self.p.sell("ACME", 50, 60)
        self.assertEqual(self.p.realized, 500)

    def test_3_value(self):
        self.assertEqual(self.p.value({"ACME": 70}), 5_000 + 3_000 + 50 * 70)
