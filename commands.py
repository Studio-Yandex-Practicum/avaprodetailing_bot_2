import asyncio

from faker import Faker

from bot.core.config import settings
from bot.db.connector import setup_get_pool
from bot.db.models import Bonus, Car
from bot.db.models.business_unit import BusinessUnit
from bot.db.models.services import Service, ServiceCategory, ServiceUnit
from bot.db.models.users import User

fake = Faker('ru_RU')


async def fill_base():
    unit_obj = BusinessUnit(
        name='KMDetailing',
        address=fake.address(),
        note='Описание KMDetailing'
    )

    super_admin_obj = User(
        phone_number='+71234567890',
        role='SUPERADMIN',
        note='Классный человек суперадмин',
        business_unit_id=1
    )
    user_obj = User(
        phone_number='+70987654321',
        note='Обычный бродяга пользователь'
    )
    bonus_obj = Bonus(
        full_amount=100,
        is_accrual=True,
        user_id=2
    )

    car_obj = Car(
        brand='Toyota',
        model='Camry',
        number='А001МР97',
        car_body_type='SEDAN',
        user_id=2
    )

    category_1 = ServiceCategory(
        name='Химчистка',
    )
    category_2 = ServiceCategory(
        name='Детейлинг',
    )

    service_1_obj = Service(
        category_id=1,
        name='Чистка кожи'
    )
    service_2_obj = Service(
        category_id=1,
        name='Реставрация руля'
    )
    service_3_obj = Service(
        category_id=2,
        name='Полировка'
    )
    service_4_obj = Service(
        category_id=2,
        name='Нанесение керамики'
    )

    service_unit_1 = ServiceUnit(
        business_unit_id=1,
        service_id=1
    )
    service_unit_2 = ServiceUnit(
        business_unit_id=1,
        service_id=2
    )
    service_unit_3 = ServiceUnit(
        business_unit_id=1,
        service_id=3
    )
    service_unit_4 = ServiceUnit(
        business_unit_id=1,
        service_id=4
    )

    add_obj = [
        unit_obj,
        super_admin_obj, user_obj,
        car_obj,
        bonus_obj,
        category_1, category_2,
        service_1_obj, service_2_obj, service_3_obj, service_4_obj,
        service_unit_1, service_unit_2, service_unit_3, service_unit_4
    ]
    session_pool = await setup_get_pool(settings.database_url)
    async with session_pool() as session:
        session.add_all(add_obj)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(fill_base())
