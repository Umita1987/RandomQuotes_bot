import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboard import make_row_keyboard
from quotes import RandomFamousQuotes

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

answer_router = Router()
# category of quotes
available_type_names = ["Famous", "Movies"]
# numbers of quotes
count_of_quotes = ([str(i) for i in range(0, 11)])


class Answer(StatesGroup):
    type_name = State()
    count = State()


@answer_router.message(Answer.type_name, F.text.in_(available_type_names))
async def chosen_type(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} chose type: {message.text}")

    await state.update_data(chosen_type=message.text.lower())
    await message.answer(
        text="How many quotes do you want to receive?:",
        reply_markup=make_row_keyboard(count_of_quotes)
    )
    await state.set_state(Answer.count)


@answer_router.message(Answer.count, F.text.in_(count_of_quotes))
async def count_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    logger.info(f"User {message.from_user.id} chose count: {message.text} for type: {user_data['chosen_type']}")

    quote = RandomFamousQuotes()
    answer = await quote.get_quotes(user_data["chosen_type"], int(message.text.lower()))
    await message.answer(text=f"{answer}", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@answer_router.message(Answer.type_name)
async def type_chosen_incorrectly(message: Message):
    logger.warning(f"User {message.from_user.id} chose an incorrect type: {message.text}")

    await message.answer(
        text="I dont know this type.\n\n"
             "Please, select from the buttons below:",
        reply_markup=make_row_keyboard(available_type_names)
    )


@answer_router.message(Answer.count)
async def count_chosen_incorrectly(message: Message):
    logger.warning(f"User {message.from_user.id} chose an incorrect count: {message.text}")

    await message.answer(
        text="I dont know this number.\n\n"
             "Please, select from the buttons below:",
        reply_markup=make_row_keyboard(count_of_quotes))


@answer_router.message()
async def cmd_type_name(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} is requesting a quote type.")

    await message.answer(
        text="Do you want a quote by famous people or from popular movies?",
        reply_markup=make_row_keyboard(available_type_names)
    )
    await state.set_state(Answer.type_name)
