import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text="Привет!")
async def buy(message):
    await message.answer("Введите команду /start чтобы начать общение.")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Расчитать"), types.KeyboardButton(text="Информация")], ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=keyboard)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Расчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    man = int(10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5)
    await message.answer(f"Ваша норма калорий {man} в день")

    await state.finish()


@dp.message_handler(text="Информация")
async def inform(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
