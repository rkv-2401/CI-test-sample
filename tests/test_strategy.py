"""Clean: hand-made price series with a known shape."""
import unittest

from stocks.strategy import backtest, crossover_signals

# Flat, then a rally, then a slide: one buy, then one sell.
RALLY_THEN_SLIDE = [100.0] * 20 + [100 + 2 * i for i in range(1, 21)] + [140 - 3 * i for i in range(1, 21)]


class Signals(unittest.TestCase):
    def test_rally_then_slide_gives_buy_then_sell(self):
        actions = [a for _, a in crossover_signals(RALLY_THEN_SLIDE, short=3, long=10)]
        self.assertEqual(actions, ["buy", "sell"])

    def test_windows_must_be_ordered(self):
        with self.assertRaises(ValueError):
            crossover_signals(RALLY_THEN_SLIDE, short=10, long=5)


class Backtest(unittest.TestCase):
    def test_round_trip_ends_in_cash(self):
        result = backtest(RALLY_THEN_SLIDE, short=3, long=10)
        self.assertEqual([t[1] for t in result["trades"]], ["buy", "sell"])

    def test_no_signal_no_trades(self):
        result = backtest([100.0] * 60, short=3, long=10)
        self.assertEqual(result["trades"], [])
        self.assertEqual(result["final_value"], 10_000.0)
