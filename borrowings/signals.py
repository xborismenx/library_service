from os import getenv

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrowing
from aiogram import Bot
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")

bot = Bot(token=TOKEN)


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        message = (
            f"New borrowings:\n"
            f"User: {instance.user.first_name} {instance.user.last_name}\n"
            f"Book: {instance.book.title}\n"
            f"Borrow date: {instance.borrow_date}\n"
            f"Expected return date: {instance.expected_return_date}"
        )
        asyncio.run(send_message(message))


async def send_message(message):
    chat_id = 393532316
    await bot.send_message(chat_id=chat_id, text=message)
