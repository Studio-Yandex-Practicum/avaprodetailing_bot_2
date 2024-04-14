from aiogram import Router

from .user import user_router
from .admin import admin_router

main_router = Router(name='main_router')

main_router.include_routers(user_router, car_router, admin_router)
