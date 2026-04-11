"""
main.py – Entry point for the Telegram card game bot.

Reads the bot token from the .env file (TELEGRAM_BOT_TOKEN) and
starts polling for updates.
"""

import os
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from handlers import (
    cmd_start,
    cmd_new_game,
    cmd_join,
    cmd_game_start,
    cmd_status,
    cmd_quit,
    button_callback,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Copy .env.example to .env and fill in your token."
        )

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("newgame", cmd_new_game))
    app.add_handler(CommandHandler("join", cmd_join))
    app.add_handler(CommandHandler("gamestart", cmd_game_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("quit", cmd_quit))
    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Bot is running – press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
