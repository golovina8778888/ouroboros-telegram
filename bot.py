"""
Simple Telegram bot integration for the Ouroboros project.

This script connects a Telegram bot to the OpenRouter AI service using
environment variables defined in a `.env` file.  It listens for text
messages from users and forwards them to the OpenRouter `/chat/completions`
endpoint to generate a response.  The reply is then sent back to the
user via Telegram.

Before running this script, make sure to:

1. Install the required dependencies listed in `requirements.txt`.
2. Create a `.env` file in the project root with the following keys:
   - TELEGRAM_BOT_TOKEN
   - OPENROUTER_API_KEY
   - GITHUB_TOKEN (not used here, but reserved for other tasks)
   - TOTAL_BUDGET (optional configuration for your agent)
   - GITHUB_USER
3. Run the script with `python bot.py`.

Note: This example uses polling to receive messages from Telegram.  For a
more robust solution, consider using webhooks.

"""

import logging
import os
import json

from typing import Any

import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore
from telegram import Update  # type: ignore
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  # type: ignore


def load_config() -> None:
    """Load environment variables from a .env file if present."""
    # Attempt to load variables from .env; it's okay if the file is missing
    load_dotenv()


def call_openrouter(prompt: str) -> str:
    """Send a prompt to OpenRouter and return the assistant's reply.

    Args:
        prompt: The user's message to send to the language model.

    Returns:
        The assistant's response text, or an error message if the request fails.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return "Error: OPENROUTER_API_KEY is not set."
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        # Optional headers for attribution; you can set these in your .env file
        "HTTP-Referer": os.environ.get("APP_URL", ""),
        "X-OpenRouter-Title": os.environ.get("APP_TITLE", "Ouroboros Telegram Bot"),
    }
    payload: dict[str, Any] = {
        "model": os.environ.get("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except Exception as exc:  # Catch network errors
        logging.exception("Request to OpenRouter failed")
        return f"Error contacting OpenRouter: {exc}"
    if response.status_code != 200:
        logging.error("OpenRouter returned status %s: %s", response.status_code, response.text)
        return f"OpenRouter API error {response.status_code}: {response.text}"
    try:
        data = response.json()
        # According to OpenRouter API, the choices list contains messages
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        logging.exception("Failed to parse OpenRouter response")
        return f"Error parsing response: {exc}"


def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text(
        "Hello! I'm the Ouroboros Telegram bot.\n"
        "Send me a message and I'll respond using OpenRouter AI."
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming text messages."""
    if update.message is None:
        return
    user_text = update.message.text or ""
    # Call the model and send back the response
    reply = call_openrouter(user_text)
    update.message.reply_text(reply)


def main() -> None:
    """Start the Telegram bot."""
    load_config()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in the environment.")
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    # Register handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    # Start polling for updates
    logging.info("Starting Ouroboros Telegram bot...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
