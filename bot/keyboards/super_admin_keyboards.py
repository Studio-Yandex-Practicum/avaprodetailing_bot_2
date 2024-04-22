from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.enums import UserRole
from bot.db.models.users import User

super_admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Бизнес-юниты',
                callback_data='business_units'
            ),
            InlineKeyboardButton(
                text='Каталог услуг',
                callback_data='admin_service_catalog',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отчеты',
                callback_data='reports_for_extra',
            ),
            InlineKeyboardButton(
                text='Рассылки',
                callback_data='mailing',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Администраторы',
                callback_data='administrators',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Режим администратора',
                callback_data='switch_admin_mode'
            ),
        ],
    ]
)

role_for_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Администратор',
                callback_data='give_admin_permissions'
            ),
            InlineKeyboardButton(
                text='Старший администратор',
                callback_data='give_super_admin_permissions'
            ),
        ],
    ],
)


def ok_admin_bio(admin):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='ОК',
                    callback_data=f'admin_bio_{admin.id}'
                ),

            ],
        ],
    )
    return kb


OK_add_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='ОК',
                callback_data='invite_admin'
            ),

        ],
    ],
)


def admin_bio_for_super_admin_kb(is_active):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить ФИО',
                    callback_data='change_phone_fio'
                ),
                InlineKeyboardButton(
                    text='Изменить номер телефона',
                    callback_data='change_phone_number_admin',
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Изменить бизнес-юнит',
                    callback_data='change_business_unit',
                ),
                InlineKeyboardButton(
                    text='Изменить роль',
                    callback_data='change_role'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заблокировать' if is_active else 'Разблокировать',
                    callback_data='block_admin'
                ),
            ],
        ]
    )
    return kb


def gener_business_unit_for_admin(data):
    builder = InlineKeyboardBuilder()
    for unit in data:
        if unit.is_active:
            builder.row(
                InlineKeyboardButton(
                    text=f'{unit.name}',
                    callback_data=f'add_unit_admin_{unit.id}'
                )
            )
    return builder.as_markup()


def gener_admin_keyboard(data):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Найти клиента',
            callback_data='search_phone_number'
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Регистрация клиента',
            callback_data='search_phone_number'
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Отчеты',
            callback_data='admin_reports',
        ),
        InlineKeyboardButton(
            text='Инфо',
            callback_data='info',
        ),
    )

    if data is UserRole.SUPERADMIN:
        builder.row(
            InlineKeyboardButton(
                text='Режим настройки',
                callback_data='extra_admin'
            ),
        )

    return builder.as_markup()


def gener_list_admins(admins: list[User]):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Зарегистрировать администратора',
            callback_data='reg_new_admin'
        ),
    )
    for admin in admins:
        if admin.role is not UserRole.USER:
            role = (admin.business_unit
                    if admin.role is UserRole.ADMIN else "Суперадмин")
            builder.row(
                InlineKeyboardButton(
                    text=(
                        f'{role} - '
                        f'{admin.last_name} {admin.first_name}'
                        f' - {"Активен" if admin.is_active else "Неактивен"}'),
                    callback_data=f'admin_bio_{admin.id}'
                )
            )

    return builder.as_markup()


super_admin_back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='extra_admin'
            )
        ]
    ]
)

send_mailing_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отправить',
                callback_data='send_mailing'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отменить',
                callback_data='extra_admin'
            )
        ],
    ]
)
