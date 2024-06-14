import pytest
import asyncio
from fastapi_cache import FastAPICache
from typing import AsyncGenerator, Iterator
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from redis import asyncio as aioredis
from fastapi.testclient import TestClient

from main import app
from core import settings, Base, db_helper


class DatabaseHelperTest:
    def __init__(self, url, echo):
        self.engine_test = create_async_engine(
            url=url,
            echo=True,
            poolclass=NullPool,
        )
        self.session_factory_test = async_sessionmaker(
            bind=self.engine_test,
            autoflush=False,
            expire_on_commit=False,
        )

    async def session_dependency_test(self):
        async with self.session_factory_test() as sess:
            yield sess
            await sess.close()


db_helper_test = DatabaseHelperTest(url=settings.get_db_url_test, echo=False)

app.dependency_overrides[db_helper.session_dependency] = (
    db_helper_test.session_dependency_test
)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with db_helper_test.engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with db_helper_test.engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        redis = aioredis.from_url("redis://localhost")
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield ac
