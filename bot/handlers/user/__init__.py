from aiogram import Router

from . import plags, profile, registration, services, start

user_router = Router(name=__name__)
user_router.include_routers(
    start.router, registration.router,
    profile.router, services.router,
    plags.router
)
