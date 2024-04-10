from aiogram import types, Router, F
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Bonus, User, BonusHistory
from bot.core.enums import UserRole, BonusType

router = Router(name=__name__)


@router.message(F.text == 'Пополнение')
async def admin_earn_points(message: types.Message, session: AsyncSession):
    """
    Обработчик команды /Сброс.
    Позволяет администратору пополнять бонусные баллы у пользователя.
    """
    user_id = message.from_user.id
    result = await session.scalars(select(User).where(User.id == user_id))
    user = result.first()
    if user and user.role == UserRole.ADMIN:
        try:
            user_to_give_points_id = int(message.text.split()[1])
            points_to_give = int(message.text.split()[2])
            user_bonus = session.query(Bonus).filter(Bonus.user_id == user_to_give_points_id).first()
            if user_bonus:
                user_bonus.full_amount += points_to_give
                session.add(BonusHistory(bonus_id=user_bonus.id, amount=points_to_reset))
                session.commit()
                await message.answer(f"Пользователю с id {user_to_give_points_id} начислено {points_to_give} бонусных баллов.")
            else: 
                await message.answer("Указанный пользователь не найден.")
        except (IndexError, ValueError):
            await message.answer("Неверный формат команды. Используйте /Пополнение <user_id> <amount>")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


@router.message(F.text == 'Списание')
async def admin_reset_points(message: types.Message, session: AsyncSession):
    """
    Обработчик команды /Сброс.
    Позволяет администратору списать бонусные баллы у пользователя.

    """
    user_id = message.from_user.id
    result = await session.scalars(select(User).where(User.id == user_id))
    user = result.first()

    if user and user.role == UserRole.ADMIN:
        try:
            user_to_reset_id, points_to_reset = map(int, message.text.split()[1:])
            user_bonus = await session.scalars(select(Bonus).where(Bonus.user_id == user_to_reset_id)).first()
            if user_bonus:
                available_points = user_bonus.full_amount - user_bonus.used_amount
                if points_to_reset > available_points:
                    points_to_reset = available_points

                user_bonus.used_amount += points_to_reset
                session.add(BonusHistory(bonus_id=user_bonus.id, amount=points_to_reset))
                session.commit()
                await message.answer(f"У пользователя с ID {user_to_reset_id} списано {points_to_reset} бонусных баллов.")
            else:
                await message.answer("Указанный пользователь не найден.")
        except (IndexError, ValueError):
            await message.answer("Неверный формат команды. Используйте /Списание <user_id> <amount>")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


@router.message(F.text == 'Баланс')
async def check_points(message: types.Message, session: AsyncSession):
    """
    Проверяет баланс бонусных баллов пользователя
    и отправляет сообщение с текущим балансом.
    """
    user_id = message.from_user.id
    result = await session.scalars(select(Bonus).where(Bonus.user_id == user_id))
    user_bonus = result.first()
    if user_bonus:
        remaining_points = user_bonus.full_amount - user_bonus.used_amount
        await message.answer(f"Ваши бонусные баллы: {remaining_points}")
    else:
        await message.answer("У вас еще нет бонусных баллов.")


@router.message(F.text == 'История')
async def show_bonus_history(message: types.Message, session: AsyncSession):
    user_id = message.from_user.id
    result = await session.scalars(
        select(BonusHistory).join(Bonus).where(Bonus.user_id == user_id).order_by(BonusHistory.date.desc())
    )
    history = result.all()

    if not history:
        await message.answer("У вас пока нет истории операций с бонусами.")
        return

    message_text = "История операций с бонусами:\n\n"
    for item in history:
        amount_str = f"+{item.amount}" if item.type == BonusType.ACCRUAL else f"-{item.amount}"
        message_text += f"{item.date.strftime('%d.%m.%Y %H:%M')}: {amount_str} ({item.type})\n"
    await message.answer(message_text)
