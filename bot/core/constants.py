DEFAULT_BALANCE = 0
SHORT_STRING_SIZE = 20

MAX_LENGTH_BIRTH_DATE = 11

DEFAULT_STRING_SIZE = 120
LONG_STRING_SIZE = 255

DEFAULT_USER_ROLE = 'Пользователь'

WELCOME_MESSAGE = 'Привет'
WELCOME_REG_MESSAGE = 'Для использования бота необходима регистрация'
WELCOME_ADMIN_MESSAGE = 'Привет админ, нужно доработать текст'
WELCOME_SUPER_ADMIN_MESSAGE = 'Привет супр админ, доработать текст'
STATE_FIO = 'Введите ФИО в формате Иванов Иван Иванович'
STATE_BIRTH_DATE = 'Введите дату рождения в формате 01.02.3000'
STATE_PHONE_NUMBER = 'Введите номер телефона в формате +78888888888'
THX_REG = (
    f'Спасибо за регистрацию!\n'
    f'Вам начислено 100 приветственных баллов.\n'
    'Дополните, пожалуйста, Ваш профиль информацией по автомобилю. '
    'Так мы сможем предложить наиболее подробный перечень услуг.'
)



PROFILE_MESSAGE_WITH_INLINE = 'Выберите пункт меню'

# admin_client + update_profile
CLIENT_BIO = (
    'Профиль клиента:\n'
    'ФИО {last_name} {first_name}\n'
    'Дата рождения {birth_date}\n'
    'Номер телефона {phone_number}\n'
    'Баланс <Баланс> бонусов\n'
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

ERROR_MESSAGE = (
    'Неверный формат ввода\n'
    '{info_text}\n'
    'Вы ввели {incorrect}'
)