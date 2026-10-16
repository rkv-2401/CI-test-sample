"""Cash, holdings in first-in-first-out lots, and realised profit."""
from collections import defaultdict, deque


class InsufficientFunds(Exception):
    pass


class InsufficientShares(Exception):
    pass


class Portfolio:
    def __init__(self, cash, fee=0.0):
        self.cash = cash
        self.fee = fee
        self.realized = 0.0
        self._lots = defaultdict(deque)  # symbol -> deque of [shares, price]

    def buy(self, symbol, shares, price):
        cost = shares * price + self.fee
        if shares <= 0:
            raise ValueError("shares must be positive")
        if cost > self.cash:
            raise InsufficientFunds(f"need {cost:.2f}, have {self.cash:.2f}")
        self.cash -= cost
        self._lots[symbol].append([shares, price])

    def sell(self, symbol, shares, price):
        if shares <= 0:
            raise ValueError("shares must be positive")
        if shares > self.shares(symbol):
            raise InsufficientShares(f"want {shares}, hold {self.shares(symbol)}")
        remaining, lots = shares, self._lots[symbol]
        while remaining:
            lot = lots[0]
            n = min(remaining, lot[0])
            self.realized += n * (price - lot[1])
            lot[0] -= n
            remaining -= n
            if lot[0] == 0:
                lots.popleft()
        self.cash += shares * price - self.fee
        self.realized -= self.fee

    def shares(self, symbol):
        return sum(n for n, _ in self._lots[symbol])

    def value(self, prices):
        """Cash plus every holding at the given {symbol: price}."""
        return self.cash + sum(self.shares(s) * prices[s] for s in self._lots)
