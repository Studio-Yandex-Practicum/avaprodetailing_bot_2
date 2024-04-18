import re
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import MAX_LENGTH_BIRTH_DATE
from bot.core.enums import UserRole
from bot.db.crud.users import users_crud
from bot.db.models.car import Car
from bot.db.models.users import User


def verify_symbols(num):
    special_characters = "!@#$%^&*()-+?_=, <>/'\""
    return not any(c in special_characters for c in num)


async def check_user_is_none(
    tg_id: int,
    session: AsyncSession,
) -> None:
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    return user is None


async def check_user_is_admin(
    tg_id: int,
    session: AsyncSession,
) -> None:
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    return user.role is UserRole.ADMIN


async def validate_fio(msg: str):
    check = r'^[А-ЯЁ]([а-я]*)\s[А-ЯЁ]([а-я]*)'
    match = re.match(check, msg)
    return match is not None


async def validate_birth_date(msg: str):
    check = r'^(([0][1-9]|[1][0-9])|([2][0-9])|([3][0-1])|([1-9]))\.(([0][1-9])|([1][0-2])|[1-9])\.[1-2]([0-9]..)'
    current_date = date.today()
    match = re.match(check, msg)
    if match is not None and len(msg) < MAX_LENGTH_BIRTH_DATE:
        birth_date = datetime.strptime(msg, '%d.%m.%Y').date()
        if (
            (current_date > birth_date) and
            (birth_date.year in range(
                current_date.year - 100, current_date.year - 16
            ))
        ):
            return True
    return False


async def validate_phone_number(phone_number: str):
    pattern = r'^\+\d{6,20}$'
    return re.match(pattern, phone_number) is not None
