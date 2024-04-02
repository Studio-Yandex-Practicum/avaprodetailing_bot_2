from db.models import Services
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession


async def price(
        price: int,
        session: AsyncSession
) -> Services:
    service = await service_crud.get(
        obj_id=price, session=session
    )
    if service == 0:
        raise ValidationError('Уточнять у администратора')
    return service
