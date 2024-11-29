import asyncio
from os import getenv

from dotenv import load_dotenv
from notifications.bot import bot

from notifications.borrowers import borrowers_overdue

load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")
chat_id = getenv("CHAT_ID")


def overdue_borrowings():
    message = borrowers_overdue()
    asyncio.run(send_message(message, chat_id))


async def send_message(message: str, chat: int) -> None:
    await bot.send_message(chat_id=chat_id, text=message)
