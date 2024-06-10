# Create Read Update Delete
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import Person
from .schemas import PersonSchemaCreate


async def create_person(
    session: AsyncSession,
    new_person: PersonSchemaCreate,
) -> Person:
    person = Person(**new_person.model_dump())
    session.add(person)
    await session.commit()
    return person


async def find_person_by_id(
    session: AsyncSession,
    id: int,
) -> Person:
    return await session.get(Person, id)


async def find_person_by_email(
    session: AsyncSession,
    email: EmailStr,
) -> Person:
    stmt = select(Person).where(Person.email == email)
    result = await session.execute(stmt)
    person = result.scalar()
    return person


async def delete_person_by_id(
    session: AsyncSession,
    person: Person,
) -> None:
    await session.delete(person)
    await session.commit()
