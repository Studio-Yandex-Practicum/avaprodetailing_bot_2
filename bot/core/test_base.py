from datetime import datetime as dt

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.enums import BonusType
from bot.db.models.bonus import Bonus, BonusCase
from bot.db.models.business_unit import BusinessUnit
from bot.db.models.car import Car
from bot.db.models.services import Service, ServiceCategory, ServiceUnit
from bot.db.models.users import User

fake = Faker('ru_RU')


async def test_base(session: AsyncSession):
    last_name, first_name, middle_name = [x for x in fake.name().split()]

    user_obj = User(
        phone_number=fake.phone_number(),
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        birth_date=dt.strptime(fake.date(), '%Y-%m-%d').date(),
    )

    bonus_obj = Bonus(
        used_amount=11,
        full_amount=11,
        start_date=dt.now(),
        is_active=1,
        user_id=1,
    )

    unit_obj = BusinessUnit(
        name='unit',
        address=fake.address(),
        is_active=1,
    )

    bonuscase_obj = BonusCase(
        name='BonusCase',
        type=BonusType.ACCRUAL,
    )

    car_obj = Car(
        brand='brand',
        model='model',
        user_id=1
    )

    service_cat_obj = ServiceCategory(
        name='name',
        is_active=1
    )

    servcie_obj = Service(
        category_id=1,
        is_active=1
    )

    ser_unit_obj = ServiceUnit(
        business_unit_id=1,
        service_id=1,
    )

    add_obj = [
        user_obj, bonus_obj, unit_obj, bonuscase_obj, car_obj, service_cat_obj,
        servcie_obj, ser_unit_obj
    ]
    session.add_all(add_obj)
    await session.commit()
