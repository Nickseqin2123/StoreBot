import logging
import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from main_router import router as main_rout
from keyboards.keyboards import menu
from SqlRequest.RequestsSecond import database


dp = Dispatcher()
dp.include_router(
    main_rout
)


@dp.message(CommandStart())
async def start_menu(message: Message):
    database.set_user(message.from_user.id)
    await message.answer(
        text="Добро пожаловать в мой магазин :>",
        reply_markup=menu(message.from_user.id)
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token="7132163630:AAGoLaHji_7SL3kAc8TfVh66aJj7TDQhHgY")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())