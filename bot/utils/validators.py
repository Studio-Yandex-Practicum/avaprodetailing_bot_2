from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.users_crud import user_crud


async def check_user_from_db(
    tg_id: int,
    session: AsyncSession,
) -> None:
    user = await user_crud.get(
        obj_id=tg_id, session=session
    )
    if user is not None:
        return False
    return True