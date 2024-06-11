from fastapi import APIRouter

from .shop.views import router as shop_router
from .person.views import router as person_router

router = APIRouter()
router.include_router(person_router)
router.include_router(shop_router)
