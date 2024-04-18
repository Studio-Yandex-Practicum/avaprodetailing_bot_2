from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import DEFAULT_STRING_SIZE, LONG_STRING_SIZE
from bot.db.models.base import Base
from bot.db.models.users import User


class BusinessUnit(Base):
    __tablename__ = 'business_units'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    address: Mapped[str] = mapped_column(String(LONG_STRING_SIZE))
    note: Mapped[Optional[str]] = mapped_column(String(LONG_STRING_SIZE))
    is_active: Mapped[bool] = mapped_column(default=True)
    admin_users: Mapped[set['User']] = relationship(
        back_populates='business_unit',
        primaryjoin="and_(BusinessUnit.id == User.business_unit_id, "
                    "User.role == 'ADMIN')",
    )
    services: Mapped[List['Service']] = relationship(
        lazy='selectin',
        secondary='service_unit',
        back_populates='business_units'
    )

    @classmethod
    def data_to_model(cls, data):
        return cls(
            name=data.get('name'),
            note=data.get('note'),
            address=data.get('address')
        )

    def __repr__(self) -> str:
        return (f'BusinessUnit(id={self.id},'
                f' name={self.name}, address={self.address})')
