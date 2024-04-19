from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import REGISTRATION_BONUS_AMOUNT
from bot.db.crud.bonus import bonuses_crud
from bot.db.models import User


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
