from urllib import response
from requests import session
from sqlalchemy import insert, select, delete

from core import Shop, Person
from httpx import AsyncClient
from conftest import client, db_helper_test


async def test_create_shop(ac: AsyncClient):
    response = await ac.post(
        "/shop/", json={"title": "DNS", "rating": 3, "compensation": 10_000}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "DNS"


async def test_get_shop(ac: AsyncClient):
    response = await ac.get("/shop/", params={"shop_title": "DNS"})
    assert response.status_code == 200
    assert response.json()["title"] == "DNS"


async def test_update_shop(ac: AsyncClient):
    response = await ac.patch(
        "/shop/",
        params={"shop_title": "DNS"},
        json={"title": "Sulpak", "compensation": 180},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Sulpak"


async def test_delete_shop(ac: AsyncClient):
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Shop).values(title="Mechta", rating=4, compensation=13000)
        await session.execute(stmt)
        await session.commit()

    response = await ac.delete(
        "/shop/",
        params={"shop_title": "Mechta"},
    )
    assert response.status_code == 204


async def test_work_registration(ac: AsyncClient):
    response = await ac.post(
        "/shop/work", params={"shop_title": "Sulpak", "person_email": "react@gmail.com"}
    )
    assert response.status_code == 202


async def test_get_shop_workers(ac: AsyncClient):
    response = await ac.get("/shop/shop_workers", params={"title": "Sulpak"})
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_get_work_of_person(ac: AsyncClient):
    response = await ac.get(
        "/shop/work_of_person/{email}", params={"person_email": "react@gmail.com"}
    )
    assert response.status_code == 202
    assert response.json() == "Sulpak"


async def test_get_all_persons_with_works(ac: AsyncClient):
    response = await ac.get("/shop/persons_with_shops")
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_update_workplace_for_person(ac: AsyncClient):
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Shop).values(title="DNS", rating=5, compensation=12000)
        await session.execute(stmt)
        await session.commit()

    response = await ac.patch(
        "/shop/update_workplace",
        params={"shop_title": "DNS", "person_email": "react@gmail.com"},
    )
    assert response.status_code == 200
    # assert response.json()["work_place_name"] == "DNS"


async def test_delete_workplace_of_person(ac: AsyncClient):
    response = await ac.delete(
        "/shop/work_place", params={"person_email": "react@gmail.com"}
    )
    assert response.status_code == 204
