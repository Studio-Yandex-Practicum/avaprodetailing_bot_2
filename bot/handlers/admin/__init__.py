from aiogram import Router

from . import payment
from . import admin_client

admin_router = Router(name=__name__)
admin_router.include_routers(payment.router, admin_client.router)
