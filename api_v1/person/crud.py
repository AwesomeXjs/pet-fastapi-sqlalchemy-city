# Create Read Update Delete
from pydantic import EmailStr
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import Person
from .schemas import PersonSchemaCreate, PersonSchemaUpdate, PersonSchemaUpdatePartial


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


async def find_all_persons(session: AsyncSession) -> list[Person]:
    stmt = select(Person).options(selectinload(Person.work_place)).order_by(Person.id)
    res: Result = await session.execute(stmt)
    persons = res.scalars().all()
    return list(persons)


async def delete_person_by_id(
    session: AsyncSession,
    person: Person,
) -> None:
    await session.delete(person)
    await session.commit()


async def update_person(
    session: AsyncSession,
    person: Person,
    person_update: PersonSchemaUpdatePartial,
) -> Person:
    for name, value in person_update.model_dump(exclude_unset=True).items():
        setattr(person, name, value)
    await session.commit()
    return person
