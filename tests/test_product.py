from urllib import response
from sqlalchemy import insert
from httpx import AsyncClient
from core import Shop, Product
from conftest import db_helper_test


async def test_create_product(ac: AsyncClient):
    response = await ac.post(
        "/product/", json={"title": "Eggs", "type": "Food", "price": 20}
    )
    assert response.status_code == 200, "Продукт не создан"
    assert response.json()["title"] == "Eggs"


async def test_get_product(ac: AsyncClient):
    response = await ac.get("/product/", params={"title": "Eggs"})
    assert response.status_code == 200, "Продукт не найден"


async def test_update_product(ac: AsyncClient):
    response = await ac.patch(
        "/product/",
        params={"title": "Eggs"},
        json={"title": "Milk", "price": 450},
    )
    assert response.status_code == 200, "Продукт не изменен"
    assert response.json()["title"] == "Milk"


async def test_delete_product(ac: AsyncClient):

    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Product).values(title="Display", type="Tech", price=5000)
        await session.execute(stmt)
        await session.commit()

    response = await ac.delete("/product/", params={"title": "Display"})
    assert response.status_code == 200, "Продукт не удален"


async def test_add_product_to_shop(ac: AsyncClient):
    async with db_helper_test.session_factory_test() as session:
        stmt = insert(Shop).values(title="Dostik", rating=5, compensation=10222)
        await session.execute(stmt)
        await session.commit()

        stmt = insert(Product).values(title="Mouse", type="Tech", price=5000)
        await session.execute(stmt)
        await session.commit()

    response = await ac.post(
        "/product/add_product",
        params={
            "title": "Mouse",
            "shop_title": "Dostik",
        },
    )
    print(response)
    assert response.status_code == 200


async def test_get_products_by_shop(ac: AsyncClient):
    response = await ac.get("/product/by_shop", params={"title": "Dostik"})
    assert response.status_code == 200, "Продукты конкретного магазина не найдены"


async def test_get_all_shops_with_products(ac: AsyncClient):
    response = await ac.get("/product/all_shops")
    assert response.status_code == 200, "Магазины с продуктами не найдены"
    assert len(response.json()) > 0
