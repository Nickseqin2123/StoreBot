from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from SqlRequest.RequestsSecond import database
from keyboards.keyboards import menu


router = Router(name=__name__)


@router.message(F.text == "Удалить товар из корзины")
async def delete_product_user(message: Message):
    card = database.get_user_card(message.from_user.id)

    if card:
        for i in card:
            builder = InlineKeyboardBuilder()

            builder.add(
                InlineKeyboardButton(
                    text="Удалить товар",
                    callback_data=f"deleteusercard {i['product']} {i['count']} {i['price']}"
                )
            )
            await message.answer(
                text=f"""
Название товара: {i["product"]}
Кол-во в корзине: {i["count"]}
Цена: {i["price"]} рублей""", reply_markup=builder.as_markup(resize_keyboard=True)
            )
        await message.answer(
            text="Выберите товар который хотите удалить"
        )
    else:
        await message.answer(
            text="Ваша корзина пуста"
        )


@router.callback_query(F.data.split()[0] == "deleteusercard")
async def deli(callback: CallbackQuery):
    pr = callback.data.split()

    database.delete_user_card(
        callback.from_user.id,
        pr[1],
        int(pr[2]),
        int(pr[-1])
    )
    await callback.message.answer(
        text=f"Товар {pr[1]} был удален из вашей корзины",
        reply_markup=menu(callback.from_user.id)
    )
    await callback.message.delete()
