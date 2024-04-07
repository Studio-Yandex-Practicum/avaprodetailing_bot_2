from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from bot.core.constants import DEFAULT_STRING_SIZE, MAX_STRING_SIZE
from .base import Base


class ServiceUnit(Base):

    __tablename__ = 'service_unit'

    id: Mapped[int] = mapped_column(primary_key=True)

    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey('business_unit.id'))
    business_unit: Mapped['Service'] = relationship(
        foreign_keys=[business_unit_id], back_populates='service_unit'
    )
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    service: Mapped['Service'] = relationship(
        foreign_keys=[service_id], back_populates='service_unit'
    )
    is_active: Mapped[bool] = mapped_column(default=True)


class Service(Base):

    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['ServiceCategory'] = relationship(
        foreign_keys=[category_id], back_populates='service'
    )
    is_active: Mapped[bool]
    note: Mapped[Optional[str]] = mapped_column(String(MAX_STRING_SIZE))


class ServiceCategory(Base):

    __tablename__ = 'service_category'

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
