from aiogram import Router

from .admin import payment_router
from .user import user_router

main_router = Router(name='main_router')

main_router.include_routers(user_router)
main_router.include_routers(payment_router)
