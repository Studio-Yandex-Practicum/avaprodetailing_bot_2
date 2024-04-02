from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.users_crud import users_crud

async def user_check_before_reg(
    tg_user_id: int,
    session: AsyncSession,
):
    #user = await users_crud.?????????
    
    if user:
        return False
    return True