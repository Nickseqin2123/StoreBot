from aiogram import Router, F
from aiogram.types import Message


router = Router(name=__name__)


async def userCard(message: Message):
    user_card = 