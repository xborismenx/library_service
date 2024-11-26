import asyncio
from os import getenv

from aiogram import Bot
from celery import shared_task

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")
bot = Bot(token=TOKEN)

@shared_task
def overdue_borrowings():

    message = "Ваше сообщение: ---"
    chat_id = 393532316

    asyncio.run(send_message(message, chat_id))


async def send_message(message, chat_id):
        await bot.send_message(chat_id=chat_id, text=message)

