"""Telegram notification module."""

from dataclasses import dataclass
from typing import Optional

try:
    from telegram import Bot
except Exception:  # pragma: no cover
    Bot = None  # type: ignore


@dataclass
class TelegramNotifier:
    """Sends Telegram messages using a bot."""

    bot_token: str
    chat_id: str
    _bot: Optional[Bot] = None

    def __post_init__(self) -> None:
        if Bot is None:  # pragma: no cover - handled via import
            raise ImportError("python-telegram-bot is required")
        self._bot = Bot(self.bot_token)

    def send_text(self, message: str) -> None:
        """Sends a text message."""
        if not self._bot:
            if Bot is None:  # pragma: no cover
                raise ImportError("python-telegram-bot is required")
            self._bot = Bot(self.bot_token)
        self._bot.send_message(chat_id=self.chat_id, text=message)
