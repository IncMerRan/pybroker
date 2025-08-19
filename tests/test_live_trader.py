from unittest.mock import Mock

from pybroker.live_trader import LiveTrader, TradeSignal


def test_live_trader_emits_signal():
    notifier = Mock()
    prices = {"BTCUSDT": 100.0}

    def fetch_price(symbol: str) -> float:
        return prices[symbol]

    def strategy(symbol: str, price: float) -> TradeSignal:
        return TradeSignal(
            symbol, "BUY", price, price * 1.03, price * 0.99, "short", 3.0
        )

    trader = LiveTrader(
        ["BTCUSDT"], notifier, fetch_price=fetch_price, interval=0
    )
    trader.start(strategy, iterations=1)
    notifier.send_text.assert_called_once()
