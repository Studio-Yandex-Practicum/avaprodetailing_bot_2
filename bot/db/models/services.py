from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from bot.core.constants import DEFAULT_STRING_SIZE, LONG_STRING_SIZE
from bot.db.models.base import Base


class ServiceUnit(Base):

    __tablename__ = 'service_unit'

    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey('business_units.id'), primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'),
                                            primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class Service(Base):

    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('service_category.id'))
    is_active: Mapped[bool] = mapped_column(default=True)
    note: Mapped[Optional[str]] = mapped_column(String(LONG_STRING_SIZE))
    business_units: Mapped[List['BusinessUnit']] = relationship(
        secondary='service_unit', back_populates='services'
    )


class ServiceCategory(Base):

    __tablename__ = 'service_category'

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
