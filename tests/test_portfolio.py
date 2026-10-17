"""Clean: each test builds its own Portfolio. Safe in any order, on any worker."""
import unittest

from stocks.portfolio import InsufficientFunds, InsufficientShares, Portfolio


class Buying(unittest.TestCase):
    def test_buy_takes_cost_and_fee(self):
        p = Portfolio(1000, fee=2)
        p.buy("ACME", 10, 50)
        # self.assertEqual(p.cash, 498)
        # Intentionally fail a test
        self.assertEqual(p.cash, 600)
        self.assertEqual(p.shares("ACME"), 10)

    def test_cannot_overspend(self):
        p = Portfolio(100)
        with self.assertRaises(InsufficientFunds):
            p.buy("ACME", 3, 40)
        self.assertEqual(p.cash, 100)

    def test_rejects_zero_shares(self):
        with self.assertRaises(ValueError):
            Portfolio(100).buy("ACME", 0, 10)


class Selling(unittest.TestCase):
    def test_sells_oldest_lot_first(self):
        p = Portfolio(10_000)
        p.buy("ACME", 10, 100)
        p.buy("ACME", 10, 200)
        p.sell("ACME", 15, 150)
        # 10 bought at 100 (+500) and 5 bought at 200 (-250)
        self.assertEqual(p.realized, 250)
        self.assertEqual(p.shares("ACME"), 5)

    def test_cannot_sell_what_you_dont_hold(self):
        p = Portfolio(1000)
        p.buy("ACME", 2, 10)
        with self.assertRaises(InsufficientShares):
            p.sell("ACME", 3, 10)

    def test_fee_reduces_realized(self):
        p = Portfolio(1000, fee=1)
        p.buy("ACME", 10, 10)
        p.sell("ACME", 10, 12)
        self.assertEqual(p.realized, 19)


class Valuing(unittest.TestCase):
    def test_value_is_cash_plus_holdings(self):
        p = Portfolio(1000)
        p.buy("ACME", 5, 100)
        p.buy("BOLT", 2, 50)
        self.assertEqual(p.value({"ACME": 120, "BOLT": 40}), 400 + 600 + 80)
