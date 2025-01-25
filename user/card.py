import json


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from requestss.user import getUserCard
from models.models import Card, Product
from keyboardd.inlines import inline
from requestss.user import deleteProductUser, addProductCountUserCard, subUserCountCard
from other.others import add_ending


router = Router(name=__name__)


class Operation(StatesGroup):
    count = State()
    
    
@router.message(F.text == 'Моя корзина')
async def user_card(message: Message):
    user_card_response: str = await getUserCard(user_id=message.from_user.id)
    
    if isinstance(user_card_response, str):
        await message.answer(
            text=user_card_response
        )
    else:
        for item in user_card_response:
            item_obj: Card = item[0]
            product: Product = item_obj.product
            
            await message.answer(text=f'''
📦 |Название продукта: ** <b>{product.name}</b> **

💰 |Цена продукта: ** <b>{product.price:.1f} руб.</b> **
💫 |У вас в корзине: ** <b>{item_obj.count} eд.</b> **
📝 |Описание продукта: ** <b><u>{product.description}</u></b> **
''', parse_mode='HTML', reply_markup=await inline(Убавить={'id': product.id, 'name': product.name, 'operation': 'sub'},
                                                  Добавить={'id': product.id, 'name': product.name, 'operation': 'add'},
                                                  Удалить={'id': product.id, 'name': product.name, 'operation': 'delete'}))


@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'sub'))
async def sub(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    product_name = data['name']
    
    morph = add_ending(f'Сколько {product_name} вы хотите убрать из корзины?', product_name)
    
    await state.update_data(product_id=data['id'], func=data['operation'])
    
    await state.set_state(Operation.count)
    
    await callback.message.answer(
        text=morph
    )
    

@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'add'))
async def add(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    product_name = data['name']
    
    morph = add_ending(f'Сколько {product_name} вы хотите добавить в корзину?', product_name)
    
    await state.update_data(product_id=data['id'], func=data['operation'])
    
    await state.set_state(Operation.count)
    
    await callback.message.answer(
        text=morph
    )


@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'delete'))
async def delete(callback: CallbackQuery):
    data: dict = json.loads(callback.data)
    
    message: str = await deleteProductUser(user_id=callback.from_user.id, product_id=data['id'])

    await callback.message.answer(
        text=message
    )
    
    
@router.message(Operation.count)
async def get_finally_data(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    
    data.update({'count': message.text})
    
    await state.clear()
    await summary(message, data, state)


async def summary(message: Message, data: dict, state: FSMContext):
    functions = {
        'add': addProductCountUserCard,
        'sub': subUserCountCard
    }
    
    count: str = data['count']
    product_id = data['product_id']
    function_call: addProductCountUserCard|subUserCountCard = functions[data['func']]
    
    if count.isdigit():
        response: str = await function_call(user_id=message.from_user.id,
                                           product_id=product_id,
                                           count_change=abs(int(count)))
        
        await message.answer(
            text=response
        )
    else:
        await message.answer(
            text='Вы ввели не число. Введите число:'
        )
        await state.update_data(product_id=product_id, func=data['func'])
        await state.set_state(Operation.count)
        