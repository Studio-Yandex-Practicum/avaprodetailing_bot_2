from aiogram import Router

from . import admin_client, update_profile, bonus_management, payment, info

admin_router = Router(name=__name__)
admin_router.include_routers(
    payment.router,
    admin_client.router,
    update_profile.router,
    bonus_management.router,
    info.router
)
