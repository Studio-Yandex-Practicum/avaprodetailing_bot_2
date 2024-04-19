from aiogram import Router

from . import admin_client, payment, update_profile

admin_router = Router(name=__name__)
admin_router.include_routers(payment.router,
                             admin_client.router,
                             update_profile.router)
