"""Simple live trading loop for cryptocurrencies."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

import requests

from .notification import TelegramNotifier


@dataclass
class TradeSignal:
    symbol: str
    action: str
    price: float
    tp: float
    sl: float
    term: str
    profit_pct: float


class LiveTrader:
    """Monitors symbols and emits trade signals."""

    def __init__(
        self,
        symbols: Iterable[str],
        notifier: TelegramNotifier,
        fetch_price: Optional[Callable[[str], float]] = None,
        interval: float = 60,
    ) -> None:
        self.symbols = list(symbols)
        self.notifier = notifier
        self.fetch_price = fetch_price or self._fetch_price
        self.interval = interval
        self._running = False

    def _fetch_price(self, symbol: str) -> float:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/price",
            params={"symbol": symbol},
        )
        resp.raise_for_status()
        return float(resp.json()["price"])

    def start(
        self,
        strategy: Callable[[str, float], Optional[TradeSignal]],
        iterations: Optional[int] = None,
    ) -> None:
        """Starts the trading loop."""
        self._running = True
        loop = 0
        while self._running and (iterations is None or loop < iterations):
            for symbol in self.symbols:
                price = self.fetch_price(symbol)
                signal = strategy(symbol, price)
                if signal and signal.action == "BUY":
                    msg = (
                        f"BUY {signal.symbol} at {signal.price:.2f}\n"
                        f"TP: {signal.tp:.2f}\n"
                        f"SL: {signal.sl:.2f}\n"
                        f"Term: {signal.term}\n"
                        f"Profit %: {signal.profit_pct:.2f}"
                    )
                    self.notifier.send_text(msg)
            loop += 1
            time.sleep(self.interval)

    def stop(self) -> None:
        self._running = False
