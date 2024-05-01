from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboards import menu
from SqlRequest.RequestsSecond import database


router = Router(name=__name__)


class SelectProdForSub(StatesGroup):
    su = State()
    

@router.callback_query(F.data.split()[0] == "subusrpr")
async def clbck_sub_user(callback: CallbackQuery, state: FSMContext):
    cbc = callback.data.split()[2:]
    
    await callback.message.delete()
    await state.clear()
    await state.update_data(prod_for_sub=cbc)
    await state.set_state(SelectProdForSub.su)
    
    cbc = callback.data.split()[2:]
        
    await callback.message.answer(
        text=f"Укажите кол-во {cbc[0]}, которого хотите убрать из корзины"
    )


@router.message(F.text == "Главное меню")
async def go_to_menu(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        text="Мы в меню",
        reply_markup=menu(message.from_user.id)
    )


@router.message(SelectProdForSub.su)
async def su(message: Message, state: FSMContext):
    await state.update_data(sub_tovar=message.text)
    
    data = await state.get_data()
    await state.clear()
    
    await summary(message, data, state)
    

async def summary(message: Message, data: dict, state: FSMContext):
    prod_name, count, price = data["prod_for_sub"]
    
    if data['sub_tovar'].isdigit():
        if int(count) - int(data['sub_tovar']) > 0:
            database.sub_product_user(
                message.from_user.id,
                prod_name,
                int(data['sub_tovar']),
                int(price)
            )
            await message.answer(
                text=f"Товар {prod_name}, уменьшен в кол-ве",
                reply_markup=menu(message.from_user.id)
            )
            return
        elif int(count) - int(data['sub_tovar']) == 0:
            database.delete_user_card(
                message.from_user.id,
                prod_name,
                int(count),
                int(price)
            )
            await message.answer(
                text=f"Товар {prod_name}, был удален из вашей корзины",
                reply_markup=menu(message.from_user.id)
            )
            return
        await state.update_data(prod_for_sub=data["prod_for_sub"])
        await state.set_state(SelectProdForSub.su)
        await message.answer(
            text="Вы ввели не числовое значение. Введите корекктное число"
        )