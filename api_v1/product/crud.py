from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import Product, Shop
from api_v1.shop.schemas import ShopWithId
from .schemas import ProductCreate, ProductUpdate


# CREATE
async def create_product(
    session: AsyncSession,
    product: ProductCreate,
) -> Product:
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    return new_product


async def add_product_to_shop(session: AsyncSession, product: Product, shop: Shop):
    shop.products.append(product)
    await session.commit()
    return {
        "status": "access",
        "detail": f"Продукт {product.title} успешно добавлен в магазин {shop.title}",
    }


# READ
async def get_product_by_title(session: AsyncSession, title: str) -> Product:
    query = (
        select(Product).where(Product.title == title).options(joinedload(Product.shops))
    )
    result: Result = await session.execute(query)
    product = result.scalar()
    return product


async def get_products_by_shop(session: AsyncSession, title: str) -> list[Product]:
    query = select(Shop).where(Shop.title == title).options(joinedload(Shop.products))
    result: Result = await session.execute(query)
    shop = result.scalar()
    return shop.products


async def get_shops_by_product(
    session: AsyncSession, product_title: str
) -> list[ShopWithId]:
    query = (
        select(Product)
        .where(Product.title == product_title)
        .options(joinedload(Product.shops))
    )
    result: Result = await session.execute(query)
    product = result.scalar()
    return product.shops


# UPDATE
async def update_product(
    session: AsyncSession,
    product: Product,
    update_product: ProductUpdate,
) -> Product:
    for name, value in update_product.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    await session.commit()
    return product


# DELETE
async def delete_product(session: AsyncSession, product: Product):
    await session.delete(product)
    await session.commit()
    return {"status": "done", "details": f"{product.title} удален"}
