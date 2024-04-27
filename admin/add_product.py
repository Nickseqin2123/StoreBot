from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from SqlRequest.RequestsSecond import database
from settings import ADMIN
from keyboards.keyboards import menu


router = Router(name=__name__)


class Select(StatesGroup):
    sele = State()


@router.message(F.text == "Добавить товар")
async def add_prod(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN:
        products = database.get_products()
        await state.set_state(Select.sele)
        
        if products:
            for i in products:
                await message.answer(
                    text=f"""
Наименование продукта: {i['product']}
Кол-во на складе: {i['count']}
Цена: {i['price']}"""
                )
            await message.answer(
                text="""Укажите имя товара, его кол-во и цену"""
            )
            
        else:
            await message.answer(
                text="На складе пусто :<. Добавте товар. Укажите имя товара, его кол-во и цену"
            )
            
    else:
        await message.answer(
            text="У вас нет права на добавление товаров на склад"
        )


@router.message(F.text == "Главное меню")
async def main_menu_go(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        text="Мы в меню",
        reply_markup=menu(message.from_user.id)
    )


@router.message(Select.sele)
async def fina(message: Message, state: FSMContext):
    await state.update_data(admin_prod=message.text)
    data = await state.get_data()
    await state.clear()
    
    await summary(message, data, state)
    

async def summary(message: Message, data: dict, state: FSMContext):
    data_sp = data["admin_prod"].split()
    
    if len(data_sp) == 3 and data_sp[1].isdigit() and data_sp[-1].isdigit():
        database.set_products_sklad(
            data_sp[0],
            int(data_sp[1]),
            int(data_sp[-1])
        )
        await message.answer(
            text="Продукты на складе пополнились",
            reply_markup=menu(message.from_user.id)
        )
    else:
        await message.answer(
            text="Данные введены не корекктно, пожалуйста повторите ввод"
        )
        await state.set_state(Select.sele)
    