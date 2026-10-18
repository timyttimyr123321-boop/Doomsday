
import os
import asyncio
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Условная дата для обратного отсчёта
DOOMSDAY = datetime(2030, 1, 1, tzinfo=timezone.utc)


def get_countdown():
    now = datetime.now(timezone.utc)
    remaining = DOOMSDAY - now

    if remaining.total_seconds() <= 0:
        return "Условная дата уже наступила!"

    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return (
        "🌍 ОБРАТНЫЙ ОТСЧЁТ\n\n"
        "⏳ До условной даты осталось:\n"
        f"📅 {days} дней\n"
        f"🕒 {hours} часов\n"
        f"⌛ {minutes} минут и {seconds} секунд\n\n"
        "⚠️ Это условный таймер, а не научный прогноз."
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(get_countdown())


async def countdown(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(get_countdown())


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("countdown", countdown))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
