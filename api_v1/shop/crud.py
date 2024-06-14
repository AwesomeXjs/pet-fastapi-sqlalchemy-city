from time import sleep
from sqlalchemy import Result, select
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core import Shop, Person
from .schemas import CreateShop, ShopAll, ShopWithId, UpdateShop


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
    stmt = (
        select(Shop)
        .where(Shop.title == title)
        .options(joinedload(Shop.workers))
        .options(joinedload(Shop.products))
    )
    result: Result = await session.execute(stmt)
    shop = result.unique().scalar()
    return shop


# добавить айди магазина в таблицу к воркеру
# зайти на сайт ввести емаил и название магазина и чтобы он добавился в список work_place
async def work_registration(session: AsyncSession, person: Person, shop: Shop):
    if person.work_place_name is None:
        setattr(person, "work_place_name", shop.title)
        await session.commit()
        # return person
        return {
            "status": "accept",
            "details": f"Пользователь {person.username} устроился на работу в магазин {shop.title}",
        }
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER, detail=f"У пользователя уже есть работа"
    )


# Read


async def get_work_by_person(person: Person):
    return person.work_place_name


async def get_workers_of_shop(session: AsyncSession, title: str) -> list[Person] | str:
    query = select(Shop).where(Shop.title == title).options(joinedload(Shop.workers))
    result: Result = await session.execute(query)
    shop = result.unique().scalar()
    print(shop.workers)
    return shop.workers


async def get_all_persons_with_works(session: AsyncSession) -> list[Person]:
    query = (
        select(Person)
        .options(joinedload(Person.work_place))
        .where(Person.work_place_name != None)
    )
    res = await session.execute(query)
    persons = res.unique().scalars().all()
    return persons


# UPDATE
async def update_shop(
    session: AsyncSession,
    shop: ShopAll,
    new_shop: UpdateShop,
) -> Shop:
    for name, value in new_shop.model_dump(exclude_unset=True).items():
        setattr(shop, name, value)
    await session.commit()
    return shop


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
