from aiogram import Router

from .admin import admin_router
from .extra import super_router
from .user import user_router

main_router = Router(name='main_router')

main_router.include_routers(user_router, admin_router, super_router)
