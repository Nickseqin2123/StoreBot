from aiogram import Router, F
from aiogram.types import Message
from mainstore.maindb import cfg
from requestss.user import getProducts
from models.models import Product
from keyboardd.common import admin_keyb
from keyboardd.inlines import inline


router = Router(name=__name__)


@router.message((F.text == 'Админ панель') & (F.from_user.id == cfg.admin)) # Берём условия в скуобки и объединяем с помощью &(Возвращает комбинированный фильтр)
async def admin(message: Message):
    await message.answer(
        text='Вы в админ панели',
        reply_markup=await admin_keyb()
    )


@router.message((F.from_user.id == cfg.admin) & (F.text == 'Склад'))
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