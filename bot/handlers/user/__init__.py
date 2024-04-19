from aiogram import Router

<<<<<<< HEAD
from . import registration, start, profile, services
=======
from . import profile, registration, start
>>>>>>> origin/develop

user_router = Router(name=__name__)
user_router.include_routers(start.router, registration.router, profile.router, services.router)
