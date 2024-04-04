from enum import Enum


class UserRole(Enum):
    USER = 'Пользователь'
    ADMIN = 'Администратор'
    SUPERADMIN = 'Суперадмин'