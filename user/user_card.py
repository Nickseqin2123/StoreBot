from aiogram import Router, F
from SqlRequest.RequestsSecond import database
from aiogram.types import Message


router = Router(name=__name__)


@router.message(F.text == "Корзина")
async def card_user(message: Message):
    card_user = database.get_user_card(message.from_user.id)
    
    if card_user:
        shet = 0
        for i in card_user:
            shet += int(i["count"]) * int(i["price"])
            await message.answer(
                text=f"""
Название товара: {i["product"]}
Кол-во в корзине: {i["count"]}
Цена: {i["price"]} рублей"""
            )
            
        await message.answer(
            text=f"Полна стоимость корзины = {shet} рублей"
        )
        
    else:
        await message.answer(
            text="Ваша корзина пуста"
        )