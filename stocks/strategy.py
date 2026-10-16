"""Moving-average crossover: buy when the short average crosses above the long one, sell on the way down."""
from .portfolio import Portfolio
from .prices import moving_average


def crossover_signals(prices, short=5, long=20):
    """[(day index, "buy" | "sell"), ...]"""
    if short >= long:
        raise ValueError("short window must be shorter than long window")
    fast, slow = moving_average(prices, short), moving_average(prices, long)
    signals, above = [], None
    for i, (f, s) in enumerate(zip(fast, slow)):
        if f is None or s is None:
            continue
        now = f > s
        if above is not None and now != above:
            signals.append((i, "buy" if now else "sell"))
        above = now
    return signals


def backtest(prices, cash=10_000.0, short=5, long=20, fee=1.0, symbol="ACME"):
    """Put all cash in on a buy signal, sell everything on a sell signal."""
    p = Portfolio(cash, fee=fee)
    trades = []
    for i, action in crossover_signals(prices, short, long):
        held = p.shares(symbol)
        if action == "buy" and held == 0:
            n = int((p.cash - fee) // prices[i])
            if n > 0:
                p.buy(symbol, n, prices[i])
                trades.append((i, "buy", n))
        elif action == "sell" and held:
            p.sell(symbol, held, prices[i])
            trades.append((i, "sell", held))
    final = p.value({symbol: prices[-1]})
    return {"final_value": final, "return_pct": 100 * (final / cash - 1), "trades": trades}
