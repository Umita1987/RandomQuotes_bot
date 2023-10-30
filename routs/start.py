from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command(commands=["start"]))
async def greetings(message: types.Message):
    await message.answer(
        "Hello, i am quotes bot. I can send you a random quote by famous people or from popular movies"
    )
