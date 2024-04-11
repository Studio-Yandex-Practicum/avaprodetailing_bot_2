import sqlite3
from datetime import date
from datetime import datetime as dt

from sqlalchemy import null
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.enums import BonusType, UserRole
from bot.db.models.bonus import Bonus, BonusCase
from bot.db.models.business_unit import BusinessUnit
from bot.db.models.car import Car
from bot.db.models.services import Service, ServiceCategory, ServiceUnit
from bot.db.models.users import User

from faker import Faker, providers

fake = Faker('ru_RU')


async def test_base(session: AsyncSession,):
    last_name, first_name, middle_name = [x for x in fake.name().split(' ')]
    db_obj =  User(
            phone_number=fake.phone_number(),
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=dt.strptime(fake.date(), '%Y-%m-%d').date(),

        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  Bonus(
            used_amount=11,
            full_amount=11,
            start_date=dt.now(),
            is_active=1,
            user_id=1,
        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  BusinessUnit(
            name='unit',
            address='алтушка',
            is_active=1,
        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  BonusCase(
            name='BonusCase',
            type=BonusType.ACCRUAL,

        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  Car(
            brand='brand',
            model='model',
            user_id=1

        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  ServiceCategory(
            name='name',
            is_active=1

        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
        
    db_obj =  Service(
            category_id=1,
            is_active=1

        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    
    
    db_obj =  ServiceUnit(
            business_unit_id=1,
            service_id=1,


        )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
