"""Example crypto trading agent with Telegram notifications."""

from __future__ import annotations

import os
from typing import List

from pybroker.live_trader import LiveTrader, TradeSignal
from pybroker.notification import TelegramNotifier

# Default top 20 cryptocurrencies by market cap.
TOP_20_SYMBOLS: List[str] = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "SOLUSDT",
    "DOGEUSDT",
    "TRXUSDT",
    "DOTUSDT",
    "MATICUSDT",
    "LTCUSDT",
    "BCHUSDT",
    "LINKUSDT",
    "ATOMUSDT",
    "XLMUSDT",
    "ETCUSDT",
    "FILUSDT",
    "ICPUSDT",
    "APTUSDT",
    "HBARUSDT",
]

# You can modify this list to track specific coins manually.
SYMBOLS: List[str] = TOP_20_SYMBOLS


def simple_strategy(symbol: str, price: float) -> TradeSignal:
    """Generates a basic BUY signal with TP/SL."""
    tp = price * 1.03  # 3% target
    sl = price * 0.99  # 1% stop
    profit_pct = (tp - price) / price * 100
    term = "short"
    return TradeSignal(
        symbol=symbol,
        action="BUY",
        price=price,
        tp=tp,
        sl=sl,
        term=term,
        profit_pct=profit_pct,
    )


def main() -> None:
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    notifier = TelegramNotifier(bot_token, chat_id)
    trader = LiveTrader(SYMBOLS, notifier)
    trader.start(simple_strategy)


if __name__ == "__main__":
    main()
