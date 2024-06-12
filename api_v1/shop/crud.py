from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core import Shop, Person
from .schemas import CreateShop


# Create read update delete
async def create_shop(
    session: AsyncSession,
    new_shop: CreateShop,
) -> Shop:
    new_shop = Shop(**new_shop.model_dump())
    session.add(new_shop)
    await session.commit()
    return new_shop


async def find_shop_by_title(session: AsyncSession, title: str) -> Shop:
    stmt = select(Shop).where(Shop.title == title).options(joinedload(Shop.workers))
    result: Result = await session.execute(stmt)
    shop = result.unique().scalar()
    return shop


# добавить айди магазина в таблицу к воркеру
# зайти на сайт ввести емаил и название магазина и чтобы он добавился в список work_place
async def work_registration(session: AsyncSession, person: Person, shop: Shop):
    setattr(person, "work_place_name", shop.title)
    await session.commit()


# Read


async def get_work_by_person(session: AsyncSession, email: str):
    query = (
        select(Person)
        .where(Person.email == email)
        .options(selectinload(Person.work_place))
    )
    result: Result = await session.execute(query)
    person = result.scalar()
    return person.work_place


async def get_workers_of_shop(session: AsyncSession, title: str) -> list[Person] | str:
    query = select(Shop).where(Shop.title == title).options(joinedload(Shop.workers))
    result: Result = await session.execute(query)
    shop = result.unique().scalar()
    print(shop.workers)
    return shop.workers


# UPDATE
async def update_work_place(session: AsyncSession, person: Person, new_place: Shop):
    setattr(person, "work_place_name", new_place.title)
    await session.commit()
    return person


# DELETE


async def delete_shop(session: AsyncSession, shop: Shop) -> None:
    await session.delete(shop)
    await session.commit()


async def delete_work_place(session: AsyncSession, person: Person) -> None:
    setattr(person, "work_place_name", None)
    await session.commit()
