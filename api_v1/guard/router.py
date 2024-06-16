from .dependencies import api_guard
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/guard_page", tags=["Guard"], dependencies=[Depends(api_guard)]
)


@router.get("/user_payment")
async def get_user_payments():
    return {
        "status": "OK",
        "data": f"Вы прошли валидацию",
    }
