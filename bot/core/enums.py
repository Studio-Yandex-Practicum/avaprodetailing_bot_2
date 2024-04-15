from enum import Enum


class UserRole(str, Enum):
    """Роль пользователя"""

    USER = 'Пользователь'
    ADMIN = 'Администратор'
    SUPERADMIN = 'Суперадмин'


class BonusType(str, Enum):
    """Тип операции над бонусами."""

    ACCRUAL = 'Начисление'
    WRITE_OFF = 'Списание'


class PaymentState(str, Enum):
    """Статус оплаты"""

    WAITING = "Ожидание"
    PAID = "Оплачено"
    NOT_PAID = "Не оплачено"


class CarBodyType(str, Enum):
    """Типы кузовов"""

    SEDAN = 'Седан'
    COUPE = 'Купе'
    HATCHBACK = 'Хэтчбек'
    LIFTBACK = 'Лифтбек'
    FASTBACK = 'Фастбэк'
    STATION_WAGON = 'Универсал'
    CROSSOVER = 'Кроссовер'
    OFFROAD = 'Внедорожник'
    PICKUP = 'Пикап'
    VAN = 'Легковой фургон'
    MINIVAN = 'Минивэн'
    COMPACT_VAN = 'Компактвэн'
    MICROVAN = 'Микровэн'
    CONVERTIBLE = 'Кабриолет'
    ROADSTER = 'Родстер'
    TARGA = 'Тарга'
    LANDAU = 'Ландо'
    LIMOUSINE = 'Лимузин'
