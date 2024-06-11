from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.person.dependencies import find_person_by_email


from . import crud
from core import db_helper
from .schemas import CreateShop, Shop
from api_v1.person.schemas import Person
from .dependencies import find_shop_depends


router = APIRouter(prefix="/shop", tags=["Actions with shops"])


@router.post(
    "/",
    response_model=Shop,
    status_code=status.HTTP_201_CREATED,
)
async def create_shop(
    new_shop: CreateShop,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_shop(
        session=session,
        new_shop=new_shop,
    )


@router.get(
    "/{title}",
    response_model=Shop,
    status_code=status.HTTP_200_OK,
)
async def get_shop_by_title(
    shop: Shop = Depends(find_shop_depends),
):
    return shop


@router.post("/work")
async def work_registration(
    session: AsyncSession = Depends(db_helper.session_dependency),
    shop: Shop = Depends(find_shop_depends),
    person: Person = Depends(find_person_by_email),
):
    return await crud.work_registration(
        session=session,
        shop=shop,
        person=person,
    )
