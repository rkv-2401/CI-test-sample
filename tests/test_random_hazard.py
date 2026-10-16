"""XDIST HAZARD 3: the global random generator, seeded once for the module.

setUpModule seeds `random` once. test_a takes the first draw, so test_b gets
the second, and test_b's expected value assumes exactly that. On a worker
where test_a didn't run first, test_b gets the first draw instead and fails.
"""
import random
import unittest

from stocks.prices import simulate_prices


def setUpModule():
    random.seed(7)


def draws(n):
    rng = random.Random(7)
    return [simulate_prices(100, 30, 0.0, 0.02, rng)[-1] for _ in range(n)]


class GlobalSeed(unittest.TestCase):
    def test_a_first_path(self):
        self.assertAlmostEqual(simulate_prices(100, 30, 0.0, 0.02, random)[-1], draws(1)[0])

    def test_b_second_path(self):
        self.assertAlmostEqual(simulate_prices(100, 30, 0.0, 0.02, random)[-1], draws(2)[1])
