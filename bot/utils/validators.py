from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.car import Car
from bot.db.models.users import User


async def check_user_exists_by_phone(phone_number: str, session: AsyncSession) -> bool:
    query = select(User).filter(User.phone_number == phone_number)
    result = await session.execute(query)
    return result.scalar() is not None


async def get_user_cars(user_id: int, session: AsyncSession) -> list[Car]:
    query = select(Car).filter(Car.user_id == user_id)
    user_cars = await session.execute(query)
    return user_cars
