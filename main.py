import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src import config
from src.db.crud import get_users
from src.db.schemas import Base

engine = create_async_engine(config.DATABASE_URL, echo=True, pool_size=20)
async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as conn:
        pass


if __name__ == '__main__':
    asyncio.run(main())
