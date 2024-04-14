from aiogram import Router

from . import car

car_router = Router(name=__name__)
car_router.include_routers(car.router)
