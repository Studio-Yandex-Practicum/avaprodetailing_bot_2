from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import PROFILE_MESSAGE_WITH_INLINE
from bot.db.crud.users import users_crud
from bot.keyboards.users_keyboards import back_menu_kb, profile_kb
from bot.utils.qr_code import generate_qrcode

router = Router(name=__name__)

profile_message = (
    'ФИО: {last_name} {first_name}\n'
    'Дата рождения: {birth_date}\n'
    'Номер телефона: {phone_number}\n'
    'Бонусы: {bonus}\n'
    '\nДля внесения изменений в информацию - обратитесь к администратору.'
)


@router.callback_query(F.data == 'history')
async def get_bonus_history(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.message.delete()
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback.from_user.id,
        session=session
    )
    message_text = ['История начислений и списаний:']
    for bonus in reversed(user.bonuses):
        message_text.append(
            f'{bonus.start_date}'
            f' {"Начисление" if bonus.is_accrual else "Списание"}'
            f' - {bonus.full_amount - bonus.used_amount} бонусов'
        )
    if len(message_text) == 1:
        message_text.append('_история отсутствует_')
    message_text.append(f'\nТекущий баланс {user.balance} баллов')
    await callback.message.answer(
        text='\n'.join(message_text),
        reply_markup=back_menu_kb,
        parse_mode=ParseMode.MARKDOWN
    )


@router.callback_query(F.data == 'profile')
async def get_profile(
    callback: CallbackQuery,
    session: AsyncSession,
):
    await callback.message.delete()
    tg_id = callback.from_user.id
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    birth_date = datetime.strftime(db_obj.birth_date, '%d.%m.%Y')
    await callback.message.answer(
        profile_message.format(
            last_name=db_obj.last_name,
            first_name=db_obj.first_name,
            birth_date=birth_date,
            phone_number=db_obj.phone_number,
            bonus=db_obj.balance,
        ),
        reply_markup=back_menu_kb
    )


@router.callback_query(F.data == 'generate_qr_code')
async def generate_qr_code(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    link = await create_start_link(
        bot, str(callback.from_user.id), encode=True
    )

    qrcode = generate_qrcode(link)
    if qrcode is None:
        await callback.message.answer('Произошла ошибка.\nПопробуйте позже')
        return
    await callback.message.answer_photo(
        photo=BufferedInputFile(qrcode, 'qrcode.png'),
        reply_markup=back_menu_kb
    )


@router.callback_query(F.data == 'menu')
async def main_user_menu(
    callback: CallbackQuery,
    session: AsyncSession,
):
    await callback.message.delete()
    await callback.message.answer(
        PROFILE_MESSAGE_WITH_INLINE,
        reply_markup=profile_kb
    )
