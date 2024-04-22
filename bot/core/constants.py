DEFAULT_BALANCE = 0
SHORT_STRING_SIZE = 20

MAX_LENGTH_BIRTH_DATE = 11

DEFAULT_STRING_SIZE = 120
LONG_STRING_SIZE = 255

REGISTRATION_BONUS_AMOUNT = 100

DEFAULT_USER_ROLE = 'Пользователь'

WELCOME_REG_MESSAGE = 'Для использования бота необходима регистрация'
WELCOME_ADMIN_MESSAGE = 'Меню администратора'
WELCOME_SUPER_ADMIN_MESSAGE = 'Меню супер-администратора'
STATE_FIO = 'Введите ФИО в формате Иванов Иван Иванович'
STATE_BIRTH_DATE = 'Введите дату рождения в формате 01.02.3000'
STATE_PHONE_NUMBER = 'Введите номер телефона в формате +78888888888'
THX_REG = (
    'Спасибо за регистрацию!\n'
    'Вам начислено 100 приветственных баллов.\n'
    'Дополните, пожалуйста, Ваш профиль информацией по автомобилю. '
    'Так мы сможем предложить наиболее подробный перечень услуг.'
)
ERROR_MESSAGE = (
    'Неверный формат ввода\n'
    '{info_text}\n'
    'Вы ввели {incorrect}'
)

PROFILE_MESSAGE_WITH_INLINE = 'Выберите пункт меню'

CLIENT_BIO = (
    'Профиль клиента:\n'
    'ФИО {last_name} {first_name}\n'
    'Дата рождения {birth_date}\n'
    'Номер телефона {phone_number}\n'
    'Баланс {balance} бонусов\n'
    'Коммент {note}'
)
REF_CLIENT_INFO = (
    'Вы регистрируете клиента:\n'
    'Номер телефона {phone_number}\n'
    '\nДанные пользователя можно отредактировать в  кабинете клиента'
)

BLOCK_MSG = (
    'Для блокировки клиента {last_name} {first_name} '
    '{phone_number} '
    'по причине {reason_block} введите ДА\n\n'
    'Введите НЕТ при ошибке и переходе к редактированию клиента\n\n'
    'Введите МЕНЮ для перехода в главное меню'
)

BONUS_LIFESPAN = "1 год"
BONUS_DESCRIPTION = (
    "Бонусная программа:\n"
    "Количество приветственных баллов: {signup_bonus}\n"
    "Срок действия баллов: {bonus_lifespan}.\n"
    "\n"
    "Бонусные баллы могут списывать 98% суммы общего чека. "
    "При списании баллов, начисление не производится.\n"
)

PAID = "Оплачено"
