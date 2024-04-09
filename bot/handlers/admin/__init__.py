from aiogram import Router

from . import payment

payment_router = Router(name=__name__)
payment_router.include_routers(payment.router)
