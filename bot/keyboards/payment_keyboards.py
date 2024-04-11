from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


payment_method_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатить наличными.",
                callback_data="cash_payment",
            )
        ],
        [
            InlineKeyboardButton(
                text="Онлайн оплата.",
                callback_data="online_payment",
            )
        ]
    ]
)
