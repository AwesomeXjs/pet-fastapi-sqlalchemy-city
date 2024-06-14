from sqlalchemy import insert, select, delete

from core import Shop
from conftest import client, db_helper_test


async def test_add_work():
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Shop).values(title="Saturn", rating=5, compensation=10000)
        await session.execute(stmt)
        await session.commit()

        query = select(Shop)
        result = await session.execute(query)
        print(result.scalars().all())


# def test_person():
#     client.post(
#         "/person",
#         json={
#             "first_name": "string",
#             "second_name": "string",
#             "years": 10,
#             "username": "string",
#             "email": "user@example.com",
#         },
#     )
