from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from bot.core.constants import (DEFAULT_STRING_SIZE, MAX_LENGHT_NOTE)
from bot.db.models.base import Base
from bot.db.models.users import User


class BusinessUnit(Base):
    __tablename__ = "business_unit"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    address: Mapped[str] = mapped_column(String(MAX_LENGHT_NOTE))
    note: Mapped[Optional[str]] = mapped_column(String(MAX_LENGHT_NOTE))
    is_active: Mapped[bool]
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_user: Mapped[Optional[User]] = relationship(
        foreign_keys=[admin_user_id],
        viewonly=True,
        primaryjoin="and(BusinessUnit.admin_user_id == User.id, User.role == 'ADMIN')"
    )

    def __repr__(self) -> str:
        return f"BusinessUnit(id={self.id}, name={self.name}, address={self.address})"