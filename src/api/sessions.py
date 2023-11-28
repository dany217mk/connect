from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src import config

engine = create_async_engine(config.DB_URL, echo=True, pool_size=20)
async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session