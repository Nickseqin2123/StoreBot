from aiogram import Router, F
from aiogram.types import CallbackQuery
from SqlRequest.RequestsSecond import database
from keyboards.keyboards import menu


router = Router(name=__name__)


@router.callback_query(F.data.split()[0] == "deletepr")
async def clbck_del(callback: CallbackQuery):
    await callback.message.delete()
    cbc = callback.data.split()[2:]
    
    database.delete_user_card(
        callback.from_user.id,
        cbc[0],
        int(cbc[1]),
        int(cbc[-1])
    )
    
    await callback.message.answer(
        text=f"Удаление {cbc[0]}а, прошло успешно",
        reply_markup=menu(callback.from_user.id)
    )