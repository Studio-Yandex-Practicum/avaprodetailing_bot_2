from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.base import CRUDBase
from bot.db.models.payment_transaction import Visit


class VisitCRUD(CRUDBase):

    async def create(self, session: AsyncSession, obj_in: dict) -> Visit:
        db_obj = Visit.data_to_model(obj_in=obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
        

payment_crud = VisitCRUD()
