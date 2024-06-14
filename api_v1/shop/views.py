from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter

from . import crud
from core import db_helper
from api_v1.person.schemas import Person
from .dependencies import find_shop_depends
from .schemas import (
    ShopAll,
    CreateShop,
    ShopWithId,
    UpdateShop,
)
from api_v1.person.dependencies import find_person_by_email


router = APIRouter(prefix="/shop", tags=["Actions with shops"])


@router.post(
    "/",
    response_model=CreateShop,
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


@router.post(
    "/work",
    status_code=status.HTTP_202_ACCEPTED,
)
async def work_registration(
    session: AsyncSession = Depends(db_helper.session_dependency),
    shop: ShopAll = Depends(find_shop_depends),
    person: Person = Depends(find_person_by_email),
):
    return await crud.work_registration(
        session=session,
        shop=shop,
        person=person,
    )


@router.get("/shop_workers", response_model=list[Person])
@cache(expire=60)
async def get_shop_workers(
    title: str, session: AsyncSession = Depends(db_helper.session_dependency)
):
    result = await crud.get_workers_of_shop(
        session=session,
        title=title,
    )
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Workers not found",
    )


@router.get(
    "/",
    response_model=ShopAll,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60)
async def get_shop(
    shop: ShopAll = Depends(find_shop_depends),
):
    return shop


@router.get(
    "/work_of_person/{email}",
    response_model=str,
    status_code=status.HTTP_202_ACCEPTED,
)
@cache(expire=60)
async def get_work_of_person(person: Person = Depends(find_person_by_email)):
    result = await crud.get_work_by_person(
        person=person,
    )
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"This person without work",
    )


@router.get("/persons_with_shops")
async def get_all_persons_with_works(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_persons_with_works(session=session)


@router.patch("/", response_model=ShopWithId)
async def update_shop(
    new_shop: UpdateShop,
    shop: ShopWithId = Depends(find_shop_depends),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_shop(
        new_shop=new_shop,
        session=session,
        shop=shop,
    )


@router.patch("/update_workplace", response_model=Person)
async def update_workplace_for_person(
    new_shop: ShopAll = Depends(find_shop_depends),
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_email),
):
    return await crud.update_work_place(
        session=session,
        person=person,
        new_place=new_shop,
    )


@router.delete("/")
async def delete_shop(
    session: AsyncSession = Depends(db_helper.session_dependency),
    shop: ShopAll = Depends(find_shop_depends),
):
    return await crud.delete_shop(session=session, shop=shop)


@router.delete("/work_place")
async def delete_work_place_of_person(
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_email),
):
    return await crud.delete_work_place(session=session, person=person)
