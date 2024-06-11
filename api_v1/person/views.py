from pydantic import EmailStr
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core import db_helper
from .dependencies import find_person_by_id, find_person_by_email
from .schemas import (
    Person,
    PersonSchemaCreate,
    PersonSchemaUpdate,
    PersonSchemaUpdatePartial,
)

router = APIRouter(prefix="/person", tags=["Actions with persons"])


# create
@router.post(
    "/",
    response_model=Person,
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


# read all
@router.get("/all", response_model=list[Person])
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
async def get_person_by_id(
    id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.find_person_by_id(id=id, session=session)


# read by email
@router.get(
    "/{email}",
    response_model=Person,
    status_code=status.HTTP_200_OK,
)
async def get_person_by_email(
    email: EmailStr,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.find_person_by_email(email=email, session=session)


# update
@router.post("/update", response_model=Person)
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
