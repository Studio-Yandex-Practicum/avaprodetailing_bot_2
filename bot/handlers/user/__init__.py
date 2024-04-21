from aiogram import Router

from . import services

from . import registration, start, profile, service

user_router = Router(name=__name__)
user_router.include_routers(start.router, registration.router, profile.router, service.router)
