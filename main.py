import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.core.config import settings
from bot.db.connector import setup_get_pool
from bot.handlers.routers import main_router
from bot.middlewares.db import DbSessionMiddleware


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Вернуться в меню"),
        ]
    )


def set_middlewares(dp: Dispatcher, session_pool: async_sessionmaker) -> None:
    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.callback_query.middleware(DbSessionMiddleware(session_pool))
    dp.edited_message.middleware(DbSessionMiddleware(session_pool))


async def main() -> None:
    storage = MemoryStorage()
    bot = Bot(settings.bot_token.get_secret_value())
    dp = Dispatcher(storage=storage)
    set_middlewares(
        dp=dp, session_pool=await setup_get_pool(db_path=settings.database_url)
    )
    await set_default_commands(bot)

    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
