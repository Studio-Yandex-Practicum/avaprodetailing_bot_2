from datetime import datetime
from aiogram.fsm.context import FSMContext

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.constants import PROFILE_MESSAGE_WITH_INLINE
from bot.db.crud.users import users_crud
from bot.keyboards.users_keyboards import (
    back_menu_kb, profile_kb,
)
from bot.utils.qr_code import generate_qrcode

router = Router(name=__name__)

not_implemented = [
    'report_client_for_admin', 'get_bonus',
    'report_for_adm', 'TODO',
    'reports_for_extra', 'admin_reports']

@router.callback_query(F.data.in_(iterable=not_implemented))
async def plugs(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    await callback.bot.send_sticker(
        chat_id=callback.from_user.id,
        sticker='CAACAgIAAxkBAAEE5ApmJWuVg0DS5KY29UTbBOHOKFzqLAAChhQAAmKy8EsG14-Zws0O-TQE'
        )
    await callback.message.answer(
        text=('Мы не успели это сделать, не бейте нас😭'
              f'\n И нажмите кнопку /start')
    )