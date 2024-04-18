from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bonus_admin = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Начислить баллы (+)",
                callback_data="add_bonus"),
            InlineKeyboardButton(
                text="Списать баллы (-)",
                callback_data="spend_bonus")
        ]
    ]
)
