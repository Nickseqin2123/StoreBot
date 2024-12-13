from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from SqlRequest.RequestsSecond import database
from settings import ADMIN
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.keyboards import menu


router = Router(name=__name__)


@router.message(F.text == "Удалить товар")
async def sub(message: Message):
    if message.from_user.id == ADMIN:
        products = database.get_products()

        if products:
            for i in products:
                builder = InlineKeyboardBuilder()
                builder.add(
                    InlineKeyboardButton(
                        text="Удалить товар",
                        callback_data=f"delete {i['product']}"
                    )
                )

                await message.answer(
                    text=f"""
    Наименование продукта: {i['product']}
    Кол-во на складе: {i['count']}
    Цена: {i['price']}""", reply_markup=builder.as_markup(resize_keyboard=True)
                )

        else:
            await message.answer(
                text="На складе пусто :<."
            )

    else:
        await message.answer(
            text="У вас нет права на удаление товаров из склада"
        )


@router.callback_query(F.data.split()[0] == "delete")
async def callback_que(callback: CallbackQuery):
    database.delete_product(
        callback.data.split()[-1]
    )
    await callback.message.answer(
        text="Товар удален из склада",
        reply_markup=menu(ADMIN)
    )
    await callback.message.delete()
