from aiogram.utils.keyboard import ReplyKeyboardBuilder
from settings import ADMIN


def menu(user_id):
    buttons = ["Корзина", "Товары"]
    if user_id == ADMIN:
        buttons.append("Админ панель")
    
    builder = ReplyKeyboardBuilder()

    for i in buttons:
        builder.button(
            text=i
        )
    return builder.as_markup(resize_keyboard=True)


def products_keyb():
    buttons = ["Главное меню"]
    builder = ReplyKeyboardBuilder()
    
    for i in buttons:
        builder.button(
            text=i
        )
    
    return builder.as_markup(resize_keyboard=True)


def admin_pan():
    buttons = ["Добавить товар", "Удалить товар", "Главное меню"]
    builder = ReplyKeyboardBuilder()
    
    for i in buttons:
        builder.button(
            text=i
        )
    
    return builder.as_markup(resize_keyboard=True)