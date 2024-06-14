from fastapi import FastAPI
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Welcome to City", lifespan=lifespan)
app.include_router(api_v1_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
        "DELETE",
        "PATCH",
        "PUT",
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
