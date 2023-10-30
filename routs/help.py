from aiogram import Router, types
from aiogram.filters import Command

help_router = Router()


@help_router.message(Command(commands=["help"]))
async def help(message: types.Message):
    await message.answer(
        "For use the bot, select a category by clicking on the button send the number of quotes you want to receive.")


