from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from settings import ADMIN
from keyboards.keyboards import menu, admin_pan


router = Router(name=__name__)


class Stg(StatesGroup):
    main_men = State()
    

@router.message(F.text == "Админ панель")
async def admi(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN:
        await message.answer(
            text="Вот ваши кнопки",
            reply_markup=admin_pan()
        )
        await state.set_state(Stg.main_men)
    
    else:
        await message.answer(
            text="У вас нет разрешения на админ панель"
        )


@router.message(F.text == "Главное меню")
async def main_menu(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        text="Мы в меню",
        reply_markup=menu(message.from_user.id)
    )