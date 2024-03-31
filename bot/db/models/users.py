from sqlalchemy import Boolean, Column, DateTime, Integer, String
from db.models.base import Base
from core.constants import MAX_LENGHT_NAME_SURNAME
from sqlalchemy_utils import PhoneNumberType

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(PhoneNumberType())
    name = Column(String(MAX_LENGHT_NAME_SURNAME), nullable=False)
    surname = Column(String(MAX_LENGHT_NAME_SURNAME), nullable=False)
    patronymic = Column(String(MAX_LENGHT_NAME_SURNAME))
    birth_date = Column(DateTime)
    # car
    # email
