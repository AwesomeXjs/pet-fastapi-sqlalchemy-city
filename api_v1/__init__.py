from fastapi import APIRouter

from .person.views import router as person_router

router = APIRouter()
router.include_router(person_router)
