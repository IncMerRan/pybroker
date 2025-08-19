from unittest.mock import patch

from pybroker.notification import TelegramNotifier


def test_telegram_notifier_sends_message():
    with patch("pybroker.notification.telegram.Bot") as mock_bot:
        notifier = TelegramNotifier("token", "chat")
        notifier.send_text("hi")
        mock_bot.assert_called_with("token")
        mock_bot.return_value.send_message.assert_called_with(
            chat_id="chat", text="hi"
        )
