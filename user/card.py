from aiogram import Router, F
from aiogram.types import Message
from requestss.user import getUserCard
from models.models import Card, Product
from keyboardd.inlines import inline


router = Router(name=__name__)


@router.message(F.text == 'Моя корзина')
async def user_card(message: Message):
    user_card_response = await getUserCard(user_id=message.from_user.id)
    
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