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


def products_keyb(card=False):
    buttons = ["Главное меню"]
    if card:
        buttons.append("Убрать товар")
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


def user_card_keb():
    buttons = ["Удалить товар из корзины", "Главное меню"]
    builder = ReplyKeyboardBuilder()

    for i in buttons:
        builder.button(
            text=i
        )

    return builder.as_markup(resize_keyboard=True)
