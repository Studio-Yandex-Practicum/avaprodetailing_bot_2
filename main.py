import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.core.config import settings
from bot.db.connector import setup_get_pool
from bot.handlers.routers import main_router
from bot.middlewares.db import DbSessionMiddleware


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
    dp.include_router(main_router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
