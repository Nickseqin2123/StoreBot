import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message


dp = Dispatcher()


@dp.message()
async def start(message: Message):
    await message.reply(text=message.text)


async def main():
    bot = Bot(token='7132163630:AAE3l_oQzV_XMkzHVJBrMFVJ76Vfk7l38Rw')
    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())