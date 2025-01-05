from aiogram import Router
from user.card import router as card_router


router = Router(name=__name__)

router.include_routers(
    card_router    
)