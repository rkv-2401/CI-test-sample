"""Price series: load from CSV, simulate, and the indicators the strategy uses."""
import csv
import math
from datetime import date


def load_prices(path):
    """Read a CSV with columns date,close. Returns [(date, close), ...] sorted by date."""
    with open(path, newline="") as f:
        rows = [(date.fromisoformat(r["date"]), float(r["close"])) for r in csv.DictReader(f)]
    return sorted(rows)


def simulate_prices(start, days, drift, volatility, rng):
    """Geometric random walk. Pass a random.Random so the caller controls the seed."""
    prices = [start]
    for _ in range(days - 1):
        shock = rng.gauss(0.0, 1.0)
        prices.append(prices[-1] * math.exp(drift - volatility**2 / 2 + volatility * shock))
    return prices


def moving_average(values, window):
    """Simple moving average; None until the window is full."""
    if window < 1:
        raise ValueError("window must be at least 1")
    out, total = [], 0.0
    for i, v in enumerate(values):
        total += v
        if i >= window:
            total -= values[i - window]
        out.append(total / window if i >= window - 1 else None)
    return out


def daily_returns(values):
    """Fractional change from one day to the next."""
    return [b / a - 1 for a, b in zip(values, values[1:])]
