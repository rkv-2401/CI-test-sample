"""XDIST HAZARD 1: one test writes a file, a later test reads it.

unittest runs methods in alphabetical order, so test_1 always writes
out/report.json before test_2 reads it. Under `pytest -n 4` the two can land
on different workers, or test_2 can run first: FileNotFoundError, or a stale
report from an earlier run. Ben's suite has the same shape: tests read plant
files under out/ that something else must build first.
"""
import unittest

from stocks.store import read_report, write_report
from stocks.strategy import backtest

SERIES = [100.0] * 20 + [100 + 2 * i for i in range(1, 21)] + [140 - 3 * i for i in range(1, 21)]


class Report(unittest.TestCase):
    def test_1_write_report(self):
        write_report(backtest(SERIES, short=3, long=10))

    def test_2_report_has_two_trades(self):
        self.assertEqual(len(read_report()["trades"]), 2)
