from aiogram import Router

from .user import user_router
from .car import car_router

main_router = Router(name='main_router')

main_router.include_routers(user_router, car_router)
