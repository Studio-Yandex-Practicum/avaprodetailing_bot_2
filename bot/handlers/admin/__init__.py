from aiogram import Router

from . import admin_client

admin_router = Router(name=__name__)
admin_router.include_routers(admin_client.router)
