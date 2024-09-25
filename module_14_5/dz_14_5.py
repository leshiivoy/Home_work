import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import initiate_db, get_all_products, is_included, add_user

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button2 = InlineKeyboardButton(text="Формула расчета", callback_data="formulas")
kb_in.row(button, button2)

kb_shop = InlineKeyboardMarkup(resize_keyboard=True)
button_shop = InlineKeyboardButton(text="Prostate support", callback_data="product_buying")
button_shop2 = InlineKeyboardButton(text="Grape seed extract", callback_data="product_buying")
button_shop3 = InlineKeyboardButton(text="Natural cranberry", callback_data="product_buying")
button_shop4 = InlineKeyboardButton(text="Magnesium citrate", callback_data="product_buying")
kb_shop.row(button_shop, button_shop2, button_shop3, button_shop4)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calc = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
button_shop = KeyboardButton(text="Купить")
button_log = KeyboardButton(text="Регистрация")
kb.row(button_calc, button_info)
kb.row(button_shop, button_log)

initiate_db()
params = get_all_products()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию: ", reply_markup=kb_in)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer(f"Man: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) + 5")
    await call.answer()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open("../dz_14_4/files/1.png", "rb") as img:
        await message.answer(f"Название: {params[0][0]} | {params[0][1]} | Цена: {params[0][2]}")
        await message.answer_photo(img)
    with open("../dz_14_4/files/2.png", "rb") as img:
        await message.answer(f"Название: {params[1][0]} | {params[1][1]} | Цена: {params[1][2]}")
        await message.answer_photo(img)
    with open("../dz_14_4/files/3.png", "rb") as img:
        await message.answer(f"Название: {params[2][0]} | {params[2][1]} | Цена: {params[2][2]}")
        await message.answer_photo(img)
    with open("../dz_14_4/files/4.png", "rb") as img:
        await message.answer(f"Название: {params[3][0]} | {params[3][1]} | Цена: {params[3][2]}")
        await message.answer_photo(img)

    await message.answer("Выберите продукт для покупки", reply_markup=kb_shop)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст: ")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост: ")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес: ")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    man = int(10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5)
    await message.answer(f"Ваша норма калорий {man} в день")
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):", reply_markup=kb)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if is_included(message.text):
        await message.answer("Пользователь уже существует, введите другое имя")
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username = data["username"]
    email = data["email"]
    age = data["age"]
    add_user(username, email, age)
    await message.answer("Регистрация успешно завершена!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
