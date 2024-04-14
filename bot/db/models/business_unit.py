from typing import Optional

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
    is_active: Mapped[bool]
    admin_users: Mapped[set['User']] = relationship(
        back_populates='business_units',
        primaryjoin="and_(BusinessUnit.id == User.business_unit_id, User.role == 'ADMIN')",
    )

    def __repr__(self) -> str:
        return f'BusinessUnit(id={self.id}, name={self.name}, address={self.address})'
