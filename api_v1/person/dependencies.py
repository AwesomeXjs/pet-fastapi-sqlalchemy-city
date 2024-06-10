from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from . import crud
from core import db_helper


async def find_person_by_id(
    id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    person = await crud.find_person_by_id(session=session, id=id)
    if person is not None:
        return person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"person with id {id} not found",
    )


async def find_person_by_email(
    email: EmailStr,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    person = await crud.find_person_by_email(session=session, email=email)
    if person is not None:
        return person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"person with email {email} not found",
    )
