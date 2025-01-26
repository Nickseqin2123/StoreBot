import json


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mainstore.maindb import cfg
from requestss.user import getProducts
from models.models import Product
from keyboardd.common import admin_keyb, start_keyb
from keyboardd.inlines import inline
from other.others import add_ending
from requestss.admin import subProduct, addProduct, deleteProduct


router = Router(name=__name__)


class OperationAdmin(StatesGroup):
    count = State()
    

@router.message(F.text == 'Админ панель', F.from_user.id == cfg.admin) # Берём условия в скуобки и объединяем с помощью &(Возвращает комбинированный фильтр)
async def admin(message: Message):
    await message.answer(
        text='Вы в админ панели',
        reply_markup=await admin_keyb()
    )


@router.message(F.text == 'Выход')
async def end(message: Message, state: FSMContext):
    data = await state.get_data()
    
    if data is None:
        return
    
    await state.clear()
    
    await message.answer(
        text='Вы в гланом меню',
        reply_markup=await start_keyb(message.from_user.id)
    )
    

@router.message(F.from_user.id == cfg.admin, F.text == 'Склад')
async def sklad(message: Message):
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
''', parse_mode='HTML', reply_markup=await inline(Убавить={'id': product.id, 'name': product.name, 'operation': 'sub_admin'},
                                                  Добавить={'id': product.id, 'name': product.name, 'operation': 'add_admin'},
                                                  Удалить={'id': product.id, 'name': product.name, 'operation': 'delete_admin'}))


@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'sub_admin'))
async def sub_admin(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    product_name = data['name']
    
    morph = add_ending(f'Сколько {product_name} вы хотите убрать из склада?', product_name)
    
    await state.update_data(product_id=data['id'], func=data['operation'])
    
    await state.set_state(OperationAdmin.count)
    
    await callback.message.answer(
        text=morph
    )


@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'add_admin'))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    data = json.loads(callback.data)
    product_name = data['name']
    
    morph = add_ending(f'Сколько {product_name} вы хотите добавить на склад?', product_name)
    
    await state.update_data(product_id=data['id'], func=data['operation'])
    
    await state.set_state(OperationAdmin.count)
    
    await callback.message.answer(
        text=morph
    )


@router.message(OperationAdmin.count)
async def get_finally_data(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    data.update({'count': message.text})
    
    await state.clear()
    await summary(message, data, state)


@router.callback_query(F.func(lambda x: json.loads(x.data).get('operation') == 'delete_admin'))
async def delete_admin(callback: CallbackQuery):
    data: dict = json.loads(callback.data)
    
    message: str = await deleteProduct(product_id=data['id'])

    await callback.message.answer(
        text=message
    )


async def summary(message: Message, data: dict, state: FSMContext):
    functions = {
        'add_admin': addProduct,
        'sub_admin': subProduct
    }
    
    count: str = data['count']
    product_id = data['product_id']
    function_call: addProduct|subProduct = functions[data['func']]
    
    if count.isdigit():
        response: str = await function_call(product_id=product_id,
                                           count_change=abs(int(count)))
        
        await message.answer(
            text=response
        )
    else:
        await message.answer(
            text='Вы ввели не число. Введите число:'
        )
        await state.update_data(product_id=product_id, func=data['func'])
        await state.set_state(OperationAdmin.count)