import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import varvara
import sqlite3

contact = sqlite3.connect('dt.db')
cursor = contact.cursor()

api = '7126517163:AAFWequQRSnzVAFPwq0M5vMTSBnM1H3EveI'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button1 = KeyboardButton(text='Формулы рассчета')
button2 = KeyboardButton(text='Купить')
button3 = KeyboardButton(text='Регистрация')
kb.row(button, button1)
kb.add(button2, button3)
kb1 = InlineKeyboardMarkup()
but = InlineKeyboardButton(text='Product1', callback_data="product_buying")
but1 = InlineKeyboardButton(text='Product2', callback_data="product_buying")
but2 = InlineKeyboardButton(text='Product3', callback_data="product_buying")
but3 = InlineKeyboardButton(text='Product4', callback_data="product_buying")
kb1.row(but, but1, but2, but3)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_answer(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    ls = varvara.get_all_products()
    for i in range(1, 5):
        tet = f'Название: {ls[i - 1][1]} | Описание: описание {ls[i - 1][2]} | Цена: {ls[i - 1][3]}'
        with open(f'foto{i}.png', 'rb') as image:
            await message.answer_photo(image, tet)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb1)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def formula(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    a = varvara.is_include(message.text)
    if a:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await state.update_data(balance=1000)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(mes, state):
    await state.update_data(email=mes.text)
    await mes.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age_for_registration(message, state):
    await state.update_data(age=message.text)
    d = await state.get_data()
    varvara.add_user(d['username'], d['email'], d['age'])


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await UserState.weight.set()
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(str(res))
    await state.finish()


@dp.message_handler()
async def unstablermessage(message):
    await message.answer('введите команду /start для начала работы бота')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
contact.close()
