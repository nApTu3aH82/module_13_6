from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инлайн клавиатура
kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_2 = InlineKeyboardButton(text='Формула рассчета', callback_data='formulas')
kb_inline.insert(inline_button_1)
kb_inline.insert(inline_button_2)
# kb_inline = ReplyKeyboardMarkup(
#     keyboard=[
#         KeyboardButton(text='Рассчитать норму калорий'),
#         KeyboardButton(text='Формула рассчета')
#     ], resize_keyboard=True
# )

# Обычная клавиатура
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация о боте')
kb_start.add(button_1)
kb_start.add(button_2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот, помогающий здоровью!', reply_markup=kb_start)


@dp.message_handler(text=['Информация о боте'])
async def set_age(message):
    await message.answer('Я бот, помогающий здоровью!')


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 х рост(см) - 5 х возраст(г) + 5')
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_text=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth_text=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_growth(message, state):
    await state.update_data(weight_text=message.text)
    data = await state.get_data()
    calories_norm = 10 * float(data['weight_text']) + 6.25 * float(data['growth_text']) - 5 * float(
        data['age_text']) + 5
    await message.answer(f'Ваша норма калорий в день: {calories_norm}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
