import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


from routs.start import start_router
from routs.help import help_router
from routs.answer import answer_router


load_dotenv()

logging.basicConfig(level=logging.INFO)


async def main():
    bot_token = os.getenv("BOT_TOKEN")
    bot = Bot(bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(answer_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
