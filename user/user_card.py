from aiogram import Router, F
from SqlRequest.RequestsSecond import database
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from keyboards.keyboards import products_keyb, menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text="Опции товара",
                    callback_data=f"options {i["product"]} {i["count"]} {i["price"]}"
                )
            )
            
            shet += int(i["count"]) * int(i["price"])
            await message.answer(
                text=f"""
Название товара: {i["product"]}
Кол-во в корзине: {i["count"]}
Цена: {i["price"]} рублей""", reply_markup=builder.as_markup(resize_keyboard=True)
            )
            
        await message.answer(
            text=f"Полна стоимость корзины = {shet} рублей",
            reply_markup=products_keyb()
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
    

@router.callback_query(F.data.split()[0] == "options")
async def clbck_opti(callback: CallbackQuery):
    dt = callback.data
    
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="Удалить товар из корзины",
        callback_data=f"deletepr {dt}"
    ), InlineKeyboardButton(
        text="Уменьшить кол-во товара в корзине",
        callback_data=f"subusrpr {dt}"
    ))
    
    await callback.message.answer(
        text=f"Укажите, что вы хотите сделать с {dt.split()[1]}?",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )