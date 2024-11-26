import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_handlers

load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main() -> None:
    register_handlers(dp, bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
