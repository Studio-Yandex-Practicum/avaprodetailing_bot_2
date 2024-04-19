from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import REGISTRATION_BONUS_AMOUNT
from bot.db.crud.bonus import bonuses_crud
from bot.db.models import Bonus, User


async def award_registration_bonus(user: User, session: AsyncSession):
    if user is not None:
        await bonuses_crud.create(
            obj_in={
                "user_id": user.id,
                "full_amount": REGISTRATION_BONUS_AMOUNT,
                "is_accrual": True
            },
            session=session
        )


async def spend_bonuses(active_bonuses: list[Bonus], bonus_amount: int):
    modified_bonuses = []
    for bonus in active_bonuses:
        amount = min(
            bonus.full_amount - bonus.used_amount,
            bonus_amount
        )
        bonus.used_amount += amount
        if bonus.used_amount == bonus.full_amount:
            bonus.is_active = False
        bonus_amount -= amount
        if bonus_amount <= 0:
            break
    return modified_bonuses
