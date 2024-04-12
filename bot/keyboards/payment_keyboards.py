from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


payment_and_bonus_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выбор оплаты", callback_data="choose_payment"),
                InlineKeyboardButton(text="Начисление бонусов", callback_data="accrual_bonus"),
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"),
            ]
        ]
    )


qr_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сканировать QRкод", callback_data="scan_qr_code"),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel_scan"),
        ]
    ]
)
