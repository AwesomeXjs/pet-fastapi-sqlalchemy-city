import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from httpx import AsyncClient
from fastapi.testclient import TestClient

from main import app
from core import settings, Base, db_helper


class DatabaseHelperTest:
    def __init__(self, url, echo):
        self.engine_test = create_async_engine(
            url=url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
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


db_helper_test = DatabaseHelperTest(url=settings.get_db_url_test, echo=True)
app.dependency_overrides[db_helper.session_dependency] = (
    db_helper_test.session_dependency_test
)


async def init_db():
    Base.metadata.create_all(bind=db_helper_test.engine_test)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with db_helper_test.engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_helper_test.engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac