from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboard import make_row_keyboard
from quotes import RandomFamousQuotes

answer_router = Router()
# category of quotes
available_type_names = ["Famous", "Movies"]
# numbers of quotes
count_of_quotes = ([str(i) for i in range(0, 11)])


class Answer(StatesGroup):
    type_name = State()
    count = State()


@answer_router.message()
async def cmd_type_name(message: Message, state: FSMContext):
    await message.answer(
        text="Do you want a quote by famous people or from popular movies?",
        reply_markup=make_row_keyboard(available_type_names)
    )

    await state.set_state(Answer.type_name)


@answer_router.message(Answer.type_name, F.text.in_(available_type_names))
async def chosen_type(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    await message.answer(
        text="How many quotes do you want to receive?:",
        reply_markup=make_row_keyboard(count_of_quotes)
    )
    await state.set_state(Answer.count)


@answer_router.message()
async def type_chosen_incorrectly(message: Message):
    await message.answer(
        text="I dont know this type.\n\n"
             "Please, select from the buttons below:",
        reply_markup=make_row_keyboard(available_type_names)
    )


@answer_router.message(Answer.count, F.text.in_(count_of_quotes))
async def count_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    quote = RandomFamousQuotes()
    answer = quote.get_quotes(user_data["chosen_type"], int(message.text.lower()))
    await message.answer(text=f"{answer}", reply_markup=ReplyKeyboardRemove()
                         )
    await state.clear()


@answer_router.message(Answer.count)
async def count_chosen_incorrectly(message: Message):
    await message.answer(
        text="I dont know this number.\n\n"
             "Please, select from the buttons below:",
        reply_markup=make_row_keyboard(count_of_quotes))
