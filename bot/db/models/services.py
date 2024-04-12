from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import DEFAULT_STRING_SIZE, LONG_STRING_SIZE
from bot.db.models.base import Base


class ServiceUnit(Base):

    __tablename__ = 'service_unit'

    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey('business_units.id'), primary_key=True
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'),
        primary_key=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)


class Service(Base):

    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey('service_categories.id')
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    note: Mapped[Optional[str]] = mapped_column(String(LONG_STRING_SIZE))
    business_units: Mapped[List['BusinessUnit']] = relationship(
        secondary='service_unit', back_populates='services'
    )


class ServiceCategory(Base):

    __tablename__ = 'service_categories'

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
