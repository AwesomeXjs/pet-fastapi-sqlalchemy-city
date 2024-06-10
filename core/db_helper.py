from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import settings


class DatabaseHelper:
    def __init__(self, url, echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as sess:
            yield sess
            await sess.close()


db_helper = DatabaseHelper(url=settings.get_db_url, echo=True)
