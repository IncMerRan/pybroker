#!/usr/bin/env bash
# Runs the crypto Telegram agent.
set -euo pipefail

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  echo "Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables." >&2
  exit 1
fi

python examples/crypto_telegram_agent.py
