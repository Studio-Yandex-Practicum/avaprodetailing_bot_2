from aiogram import Router

from . import services

from . import registration, start, profile, services, plags

user_router = Router(name=__name__)
user_router.include_routers(start.router, registration.router, profile.router, services.router, plags.router)
