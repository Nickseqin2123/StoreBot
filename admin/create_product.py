from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mainstore.maindb import cfg
from keyboardd.common import elections, admin_keyb
from requestss.admin import addProduct


router = Router(name=__name__)


class ProductForm(StatesGroup):
    name = State()
    description = State()
    price = State()
    count = State()
    

@router.message(F.text == 'Добавить новый товар', F.from_user.id == cfg.admin)
async def add_new(message: Message, state: FSMContext):
    await state.set_state(ProductForm.name)
    await message.answer(
        text='Укажите название нового товара без цифр и лишних символов: ',
        reply_markup=await elections()
    )


@router.message(ProductForm.name)
async def get_name(message: Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(name=message.text)
        await state.set_state(ProductForm.description)
        
        await message.answer(
            text='Добавьте описание товару. Если не хотите добавлять описание, просто нажмите кнопку "Пропустить"',
            reply_markup=await elections(True)
        )
    else:
        await message.answer(
            text='Вы ввели не корректное имя товара. Укажите название нового товара без цифр и лишних символов: '
        )


@router.message(ProductForm.description)
async def conti(message: Message, state: FSMContext):
    if message.text.lower() == 'пропустить':
        await state.update_data(description='Без описания')
    else:
        await state.update_data(description=message.text)
        
    await state.set_state(ProductForm.price)
    
    await message.answer(
        text='Укажите цену нового товара: '
    )


@router.message(ProductForm.price)
async def get_name(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except Exception:
        await message.answer(
            text='Вы ввели не число. Укажите цену нового товара: '
        )
    else:
        await state.update_data(price=price)
        await state.set_state(ProductForm.count)
        
        await message.answer(
            text='Укажите кол-во товара на складе: '
        )


@router.message(ProductForm.count)
async def get_name(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(count=int(message.text))

        data = await state.get_data()
        await state.clear()
        
        await summary(message, data, state)
    else:
        await message.answer(
            text='Вы ввели не корректное число. Укажите кол-во товара на складе: '
        )


async def summary(message: Message, data: dict, state: FSMContext):
    name: str = data['name']
    description: str = data['description']
    price: float = data['price']
    count: int = data['count']
    
    message_bd = await addProduct(0, count_change=count, name=name, price=price, description=description)
    
    await message.answer(
        text=message_bd,
        reply_markup=await admin_keyb()
    )