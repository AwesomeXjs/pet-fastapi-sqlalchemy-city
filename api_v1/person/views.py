from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core import db_helper
from .schemas import Person, PersonSchemaCreate
from .dependencies import find_person_by_id, find_person_by_email

router = APIRouter(prefix="/person", tags=["Actions with persons"])


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


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_id(
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_id),
):
    await crud.delete_person_by_id(session=session, person=person)


@router.delete("/email", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_email(
    session: AsyncSession = Depends(db_helper.session_dependency),
    person: Person = Depends(find_person_by_email),
):
    await crud.delete_person_by_id(session=session, person=person)
