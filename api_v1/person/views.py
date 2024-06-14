from typing import List

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core import db_helper
from .dependencies import find_person_by_id, find_person_by_email
from .schemas import (
    Person,
    PersonSchemaCreate,
    PersonSchemaUpdatePartial,
)

router = APIRouter(prefix="/person", tags=["Actions with persons"])


# create
@router.post(
    "/",
    response_model=PersonSchemaCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_person(
    new_person: PersonSchemaCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_person(
        session=session,
        new_person=new_person,
    )


@router.post("/all_persons")
async def create_all_persons(
    new_persons: List[PersonSchemaCreate],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_all_persons(
        session=session,
        new_persons=new_persons,
    )


# read all
@router.get("/all", response_model=list[Person])
@cache(expire=60)
async def get_all_persons(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.find_all_persons(session=session)


# read by id
@router.get(
    "/{id}",
    response_model=Person,
    status_code=status.HTTP_200_OK,
)
@cache(expire=60)
async def get_person_by_id(
    person: Person = Depends(find_person_by_id),
):
    return person


# read by email
@router.get(
    "/",
    response_model=Person,
    status_code=status.HTTP_200_OK,
)
async def get_person_by_email(
    person: Person = Depends(find_person_by_email),
):
    return person


# update
@router.patch("/", response_model=Person)
async def update_person(
    person_update: PersonSchemaUpdatePartial,
    person: Person = Depends(find_person_by_email),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_person(
        person=person,
        person_update=person_update,
        session=session,
    )


# delete by id
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_id(
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_id),
):
    await crud.delete_person_by_id(session=session, person=person)


# delete by email
@router.delete("/email", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_email(
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_email),
):
    await crud.delete_person_by_id(session=session, person=person)
