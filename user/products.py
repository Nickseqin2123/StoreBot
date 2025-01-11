import json

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from requestss.user import getProducts, addProductCountUserCard
from models.models import Product
from keyboardd.inlines import inline
from other.others import add_ending


router = Router(name=__name__)


class Choice(StatesGroup):
    count = State()
    

@router.message(F.text == 'Магазин')
async def store(message: Message):
    products_response = await getProducts()
    
    if isinstance(products_response, str):
        await message.answer(
            text=products_response
        )
    else:
        for item in products_response:
            product: Product = item[0]
            
            await message.answer(text=f'''
📦 |Название продукта: ** <b>{product.name}</b> **
💰 |Цена продукта: ** <b>{product.price:.1f} руб.</b> **
💫 |Кол-во на складе: ** <b>{product.count} ед.</b> **
📝 |Описание продукта: ** <b><u>{product.description}</u></b> **

🔥 Не упустите шанс приобрести наш {product.name}!
    ''', parse_mode='HTML', reply_markup=await inline(Добавить_в_корзину={'id': product.id, 'name': product.name, 'operation': 'add_card'}))
            

@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'add_card'))
async def add_card(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    product_name = data['name']
    
    morph = add_ending(f'Сколько {product_name} вы хотите добавтить в корзину?', product_name)
    
    await state.update_data(product_id=data['id'])
    
    await state.set_state(Choice.count)
    
    await callback.message.answer(
        text=morph
    )


@router.message(Choice.count)
async def get_finally_data(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    data.update({'count': message.text})
    
    await state.clear()
    
    await summary(message, data, state)


async def summary(message: Message, data: dict, state: FSMContext):
    count: str = data['count']
    product_id = data['product_id']
    
    if count.isdigit():
        response = await addProductCountUserCard(user_id=message.from_user.id,
                                           product_id=product_id,
                                           count_change=abs(int(count)))
        
        await message.answer(
            text=response
        )
    else:
        await message.answer(
            text='Вы ввели не число. Введите число:'
        )
        await state.update_data(product_id=product_id)
        await state.set_state(Choice.count)