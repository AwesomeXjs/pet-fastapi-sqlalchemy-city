from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from . import crud
from core import db_helper


async def find_person_by_id(
    person_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    person = await crud.find_person_by_id(session=session, id=person_id)
    if person is not None:
        return person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"person with id {id} not found",
    )


async def find_person_by_email(
    person_email: EmailStr,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    person = await crud.find_person_by_email(session=session, email=person_email)
    if person is not None:
        return person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"person with email {person_email} not found",
    )
