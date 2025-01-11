import json


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def inline(**kwargs):
    builder = InlineKeyboardBuilder()
    
    for text, data in kwargs.items():
        builder.add(
            InlineKeyboardButton(
                text=text.replace('_', ' '),
                callback_data=json.dumps(data, ensure_ascii=False)
            )
        )
    
    return builder.as_markup(resize_keyboard=True)