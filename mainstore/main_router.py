from aiogram import Router
from user.card import router as card_router
from user.products import router as products_router


router = Router(name=__name__)

router.include_routers(
    card_router,
    products_router
)