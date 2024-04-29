from aiogram import Router, F
from SqlRequest.RequestsSecond import database
from aiogram.types import Message
from keyboards.keyboards import user_card_keb, menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)


class Deli(StatesGroup):
    de = State()


@router.message(F.text == "Корзина")
async def card_user(message: Message, state: FSMContext):
    card_user = database.get_user_card(message.from_user.id)
    
    if card_user:
        await state.set_state(Deli.de)
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
            text=f"Полна стоимость корзины = {shet} рублей",
            reply_markup=user_card_keb()
        )
        
    else:
        await message.answer(
            text="Ваша корзина пуста"
        )


@router.message(F.text == "Главное меню")
async def go(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer(
        text="Мы в меню",
        reply_markup=menu(message.from_user.id)
    )
