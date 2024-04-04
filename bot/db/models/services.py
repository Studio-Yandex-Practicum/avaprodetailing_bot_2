from sqlalchemy import Integer, String
from db.models.base import Base
from core.constants import MAX_LENGHT, MAX_LENGHT_N
from sqlalchemy.orm import mapped_column, Mapped, validates
from sqlalchemy import ForeignKey

class ServiceUnit(Base):

    __tablename__ = 'serviceunit'

    id: Mapped[int] = mapped_column(primary_key=True)

    businesss_unit_id: Mapped[int] = mapped_column(ForeignKey('businesss_unit_id'))
    service_id:Mapped[int] = mapped_column(ForeignKey('service_id'))
    service_unit_activity: Mapped[bool]


class Service(Base):

    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(primary_key=True)

    service_categroy_id: Mapped[int] = mapped_column(ForeignKey('service_category_id'))
    service_activity: Mapped[bool]
    service_note: Mapped[str] = mapped_column(String(MAX_LENGHT_N))


class ServiceCategory(Base):

    __tablename__ = 'servicecategory'

    id: Mapped[int] = mapped_column(primary_key=True)

    category: Mapped[str] = mapped_column(String(MAX_LENGHT))
    service_category_activity: Mapped[bool]
    service_category_name: Mapped[str] = mapped_column(String(MAX_LENGHT))
    description: Mapped[str] = mapped_column(String(MAX_LENGHT))
    price: Mapped[int] = mapped_column(Integer, default=0)
    duration: Mapped[int]

    @validates('price')
    def price_summ_on_services(self, price) -> int:
        if price==0:
            return('Уточните стоимость у администратора.')
        return price

    @validates('price')
    def validate_positive_visit_summ(self, price) -> int:
        if price < 0:
            raise ValueError("Сумма платежа не может быть отрицательной.")
        return price
