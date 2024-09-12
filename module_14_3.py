import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button2 = InlineKeyboardButton(text="Формула расчета", callback_data="formulas")
kb_in.row(button, button2)

kb_in_shop = InlineKeyboardMarkup(resize_keyboard=True)
Product1 = InlineKeyboardButton(text="Продукт 1", callback_data="product_buying")
Product2 = InlineKeyboardButton(text="Продукт 2", callback_data="product_buying")
Product3 = InlineKeyboardButton(text="Продукт 3", callback_data="product_buying")
Product4 = InlineKeyboardButton(text="Продукт 4", callback_data="product_buying")
kb_in_shop.row(Product1, Product2, Product3, Product4)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calc = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
button_shop = KeyboardButton(text="Купить")
kb.row(button_calc, button_info)
kb.add(button_shop)


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью", reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию: ", reply_markup=kb_in)


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


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer(f"Man: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) + 5")

    await call.answer()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open("files/1.png", "rb") as img:
        await message.answer_photo(img, f"Название: Product{1} | Описание: описание{1} | Цена: {1 * 100}")
    with open("files/2.png", "rb") as img:
        await message.answer_photo(img, f"Название: Product{2} | Описание: описание{2} | Цена: {2 * 100}")
    with open("files/3.png", "rb") as img:
        await message.answer_photo(img, f"Название: Product{3} | Описание: описание{3} | Цена: {3 * 100}")
    with open("files/4.png", "rb") as img:
        await message.answer_photo(img, f"Название: Product{4} | Описание: описание{4} | Цена: {4 * 100}")
    await message.answer("Выберите продукт для покупки", reply_markup=kb_in_shop)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
