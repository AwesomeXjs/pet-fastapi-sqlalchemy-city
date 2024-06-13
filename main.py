from fastapi import FastAPI
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Welcome to City", lifespan=lifespan)
app.include_router(api_v1_router)
