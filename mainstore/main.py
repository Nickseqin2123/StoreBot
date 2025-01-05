import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from requestss.user import add_user
from keyboardd.common import start_keyb
from main_router import router as main_router


dp = Dispatcher()
dp.include_router(main_router)


@dp.message(CommandStart())
async def start(message: Message):
    resp = await add_user(user_id=message.from_user.id)
    print(f'Отладка: {resp}')
    
    await message.answer(
        text='Добро пожаловать в мой магазин :>',
        reply_markup=await start_keyb()
    )


async def main():
    bot = Bot(token='7132163630:AAE3l_oQzV_XMkzHVJBrMFVJ76Vfk7l38Rw')
    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())