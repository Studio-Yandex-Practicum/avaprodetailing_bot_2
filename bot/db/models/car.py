from sqlalchemy import Column, String


'''class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=PreBase)
'''
# Подразумевается, что такой Base в другом файле будет

class Car(Base):
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    number = Column(String, unique=True, nullable=False)
