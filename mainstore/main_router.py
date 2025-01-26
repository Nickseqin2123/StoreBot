from aiogram import Router
from user.card import router as card_router
from user.products import router as products_router
from admin.products import router as admin_router
from admin.create_product import router as create_product_router


router = Router(name=__name__)

router.include_routers(
    card_router,
    products_router,
    admin_router,
    create_product_router
)