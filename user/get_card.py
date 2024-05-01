from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from SqlRequest.RequestsSecond import database
from keyboards.keyboards import products_keyb, menu


router = Router(name=__name__)


class Stt(StatesGroup):
    prod = State()
    

@router.message(F.text == "Товары")
async def prod(message: Message, state: FSMContext):
    prod = database.get_products()
    
    if prod:
        await state.set_state(Stt.prod)
        
        await message.answer(
            text="Товары на складе: ",
            reply_markup=products_keyb()
        )
        
        for i in prod:
            builder = InlineKeyboardBuilder()
            
            builder.add(
                InlineKeyboardButton(
                    text="Добавить в корзину",
                    callback_data=f'buycard {i["product"]} {i["count"]} {i["price"]}'
                )
            )
            
            await message.answer(
                text=f"""
Имя товара: {i["product"]}
Кол-во на складе: {i["count"]}
Цена: {i["price"]} рублей""", reply_markup=builder.as_markup(resize_keyboard=True)
            )
            
    else:
        await message.answer(
            text="На складе нет товаров"
        )


@router.callback_query(F.data.split()[0] == "buycard")
async def callback_qur(callback: CallbackQuery, state: FSMContext):
    await state.update_data(prod=callback.data)
    
    await callback.message.answer(
        text=f"Укажите кол-во {callback.data.split()[1]} которого хотите приобрести"
    )


@router.message(F.text == "Главное меню")
async def main_men(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        text="Мы в меню",
        reply_markup=menu(message.from_user.id)
    )


@router.message(Stt.prod)
async def upd(message: Message, state: FSMContext):
    await state.update_data(user_prod=message.text)
    
    data = await state.get_data()
    await state.clear()
    
    await summary(message, data, state)
    

async def summary(message: Message, data: dict, state: FSMContext):
    pr = data["prod"].split()
    if data["user_prod"].isdigit():
        if int(pr[2]) - int(data["user_prod"]) >= 0:
            database.add_user_card(
                user_id=message.from_user.id,
                product_name=pr[1],
                count=int(data["user_prod"]),
                price=int(pr[-1])
                                   )
            await message.answer(
                text="Товар был добавлен в вашу корзину",
                reply_markup=menu(message.from_user.id)
            )
            return
    await message.answer(
        text=f"""Вы ввели не числовое значение или неверное кол-во.
Укажите кол-во {pr[1]} которого хотите приобрести"""
    )
    await state.update_data(prod=data["prod"])
    await state.set_state(Stt.prod)
    