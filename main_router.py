from aiogram import Router
from user.user_card import router as user_card_router
from user.get_card import router as get_card_router
from admin.admin_panel import router as admin_router
from admin.add_product import router as add_product_router


router = Router(name=__name__)

router.include_routers(
    user_card_router,
    get_card_router,
    admin_router,
    add_product_router
)