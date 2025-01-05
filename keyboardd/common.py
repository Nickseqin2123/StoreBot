from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def start_keyb():
    BUTTONS = {'Моя корзина', 'Магазин'}
    builder = ReplyKeyboardBuilder()

    for button_name in BUTTONS:
        builder.button(
            text=button_name
        )
    
    return builder.as_markup(resize_keyboard=True)