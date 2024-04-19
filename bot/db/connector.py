from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


async def setup_get_pool(db_path: str) -> async_sessionmaker:
    engine = create_async_engine(
        db_path,
    )

    sessionmaker_ = async_sessionmaker(
        engine, expire_on_commit=False
    )
    return sessionmaker_
