from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from bot.core.constants import (MAX_LENGHT_NAME_SURNAME,
                                MAX_LENGHT_NOTE)
from bot.db.models.base import Base


class BusinessUnit(Base):
    __tablename__ = "business_unit"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    address: Mapped[str] = mapped_column(String(MAX_LENGHT_NOTE))
    note: Mapped[str] = mapped_column(String(MAX_LENGHT_NOTE),
                                      nullable=True)
    is_active: Mapped[bool]
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_user = relationship(
        "User",
        foreign_keys=[admin_user_id],
        viewonly=True,
        primaryjoin="and(Visit.admin_user_id == User.id, User.role == 'admin')"
    )

    def __repr__(self) -> str:
        return f"BusinessUnit(id={self.id}, name={self.name}, address={self.address})"
