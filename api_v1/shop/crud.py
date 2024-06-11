from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

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
    stmt = select(Shop).where(Shop.title == title)
    result: Result = await session.execute(stmt)
    shop = result.scalar()
    return shop


# добавить айди магазина в таблицу к воркеру
# зайти на сайт ввести емаил и название магазина и чтобы он добавился в список work_place
async def work_registration(session: AsyncSession, person: Person, shop: Shop):
    setattr(person, "work_place_name", shop.title)
    await session.commit()
