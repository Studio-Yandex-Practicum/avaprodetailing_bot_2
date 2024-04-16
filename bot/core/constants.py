DEFAULT_BALANCE = 0
SHORT_STRING_SIZE = 20

MAX_LENGTH_BIRTH_DATE = 11

DEFAULT_STRING_SIZE = 120
LONG_STRING_SIZE = 255

DEFAULT_USER_ROLE = 'Пользователь'

WELCOME_MESSAGE = 'Привет'
WELCOME_REG_MESSAGE = 'Для использования бота необходима регистрация'
WELCOME_ADMIN_MESSAGE = 'Привет админ, нужно доработать текст'
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

CLIENT_BIO = (
    'Профиль клиента:\n'
    'ФИО {last_name} {first_name}\n'
    'Дата рождения {birth_date}\n'
    'Номер телефона {phone_number}\n'
    'Список авто <Марка/модель/Гос.номер>\n'
    'Баланс <Баланс> бонусов\n'
    'Коммент {note}'
)
