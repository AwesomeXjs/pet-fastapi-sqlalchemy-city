from sqlalchemy import insert

from core import Person
from httpx import AsyncClient
from conftest import db_helper_test


async def test_add_person(ac: AsyncClient):
    response = await ac.post(
        "/person/",
        json={
            "first_name": "Vlad",
            "second_name": "Chifin",
            "years": 30,
            "username": "React",
            "email": "react@gmail.com",
        },
    )
    assert response.status_code == 201, "Персона не добавлена"


async def test_get_person_by_email(ac: AsyncClient):
    response = await ac.get(
        "/person/",
        params={"person_email": "react@gmail.com"},
    )
    assert response.status_code == 200, "Персона не найдена по email"
    assert response.json()["email"] == "react@gmail.com"


async def test_update_person(ac: AsyncClient):
    response = await ac.patch(
        "/person/",
        params={"person_email": "react@gmail.com"},
        json={"username": "ReactX"},
    )
    assert response.status_code == 200, "Персона не обновлена"
    assert response.json()["username"] == "ReactX"


async def test_create_all_persons(ac: AsyncClient):
    person_one = {
        "first_name": "string",
        "second_name": "string",
        "years": 10,
        "username": "string247",
        "email": "user333@example.com",
    }
    person_two = {
        "first_name": "string",
        "second_name": "string",
        "years": 10,
        "username": "string984",
        "email": "user777@example.com",
    }
    response = await ac.post(
        "/person/all_persons",
        json=[person_one, person_two],
    )
    assert response.status_code == 200, "Список персон не добавлен"


async def test_get_all_persons(ac: AsyncClient):
    response = await ac.get("/person/all")
    assert response.status_code == 200, "Персоны не найдены"


async def test_get_person_by_id(ac: AsyncClient):
    response = await ac.get("/person/{id}", params={"person_id": 1})
    assert response.status_code == 200, "Персона не найдена по id"
    assert response.json()["username"] == "ReactX"


# DELETE
async def test_delete_person_by_id(ac: AsyncClient):
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Person).values(
            first_name="Yan",
            second_name="Shuk",
            years=31,
            username="Yamex123",
            email="eamex123@gmail.com",
        )
        await session.execute(stmt)
        await session.commit()

    response = await ac.delete("/person/", params={"person_id": 2})
    assert response.status_code == 204, "Персона не удалена по id"


async def test_delete_person_by_email(ac: AsyncClient):
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Person).values(
            first_name="Yan",
            second_name="Shuk",
            years=31,
            username="Yamex",
            email="eamex@gmail.com",
        )
        await session.execute(stmt)
        await session.commit()

    response = await ac.delete(
        "/person/email", params={"person_email": "eamex@gmail.com"}
    )
    assert response.status_code == 204, "Персона не удалена по email"


# SHOP
# async def test_add_work_to_person(ac: AsyncClient):
#     response = await ac.post(
#         "/shop/work", params={"shop_title": "DNS", "person_email": "user@example.com"}
#     )
#     assert (
#         response.json()["details"]
#         == "Пользователь string устроился на работу в магазин DNS"
#     )
#     assert response.status_code == 202
