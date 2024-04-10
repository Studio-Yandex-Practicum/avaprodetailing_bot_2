from aiogram import Router

from . import registration, start, bonus_management

user_router = Router(name=__name__)
user_router.include_routers(start.router, registration.router, bonus_management.router)
