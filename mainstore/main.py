import asyncio
import logging
import configparser

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from requestss.user import addUser
from keyboardd.common import start_keyb
from main_router import router as main_router


dp = Dispatcher()
dp.include_router(main_router)


@dp.message(CommandStart())
async def start(message: Message):
    response = await addUser(user_id=message.from_user.id)
    print(f'Отладка: {response}')
    
    await message.answer(
        text='Добро пожаловать в мой магазин :>',
        reply_markup=await start_keyb()
    )


async def main():
    settings = configparser.ConfigParser()
    settings.read('env.ini')
    token = settings['MAIN']['TOKEN']
    
    bot = Bot(token=token)
    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())