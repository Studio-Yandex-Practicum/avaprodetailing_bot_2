from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.users_crud import user_crud
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.models.users import User
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb,back_menu_kb,profile_kb
from bot.states.user_states import RegUser
from bot.utils.validators import (validate_reg_birth_date, validate_reg_fio,
                                  validate_reg_phone_number)
from datetime import datetime

router = Router(name=__name__)

# Допилить!
@router.callback_query(F.data == 'profile')
async def get_profile(
    callback: CallbackQuery,
    session: AsyncSession,
):
    
    await callback.message.delete()
    tg_id = callback.from_user.id
    db_obj = await user_crud.get(user_id=tg_id, session=session)
    birth_date = datetime.strftime(db_obj.birth_date,'%d.%m.%Y')
    await callback.message.answer(
        f'Фамилия:{db_obj.last_name}\n'
        f'Имя:{db_obj.first_name}\n'
        f'Отчество: {db_obj.middle_name}\n'
        f'Дата рождения: {birth_date}\n'
        f'Номер телефона: {db_obj.phone_number}\n'
        f'Бонусы: {"Пока пусто"}\n'
        f'Автомобили: {"Пока пусто, допилить"}\n',
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