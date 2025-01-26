from aiogram.utils.keyboard import ReplyKeyboardBuilder
from mainstore.maindb import cfg


async def start_keyb(user_id: int):
    BUTTONS = {'Моя корзина', 'Магазин'}
    
    BUTTONS.add('Админ панель') if user_id == cfg.admin else 0
    
    builder = ReplyKeyboardBuilder()

    for button_name in BUTTONS:
        builder.button(
            text=button_name
        )
    
    return builder.as_markup(resize_keyboard=True)


async def admin_keyb():
    BUTTONS = {'Склад', 'Добавить новый товар', 'Выход'}
    
    builder = ReplyKeyboardBuilder()

    for button_name in BUTTONS:
        builder.button(
            text=button_name
        )
    
    return builder.as_markup(resize_keyboard=True)


async def elections(with_you=False):
    BUTTONS = {'Выход'}
    BUTTONS.add('Пропустить') if with_you else 0
    
    builder = ReplyKeyboardBuilder()

    for button_name in BUTTONS:
        builder.button(
            text=button_name
        )
    
    return builder.as_markup(resize_keyboard=True)