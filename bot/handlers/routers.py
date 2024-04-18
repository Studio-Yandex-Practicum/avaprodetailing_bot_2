from aiogram import Router

from .user import user_router
from .admin import admin_router
from .extra import super_router

main_router = Router(name='main_router')

main_router.include_routers(user_router, admin_router, super_router)
