from bot.db.crud.base import CRUDBase
from bot.db.models.visit import Visit
from bot.db.crud.base import CRUDBase
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast





class VisitCRUD(CRUDBase[Visit]):
    async def get_multi_user_visits(
            self, session: AsyncSession,
            user
        ):
        db_objs = await session.scalars(
            select(self.model).where(self.model.user_id == user.id
                
            )
        )
        return cast(self.model, db_objs.all())

visit_crud = VisitCRUD(Visit)
