from math import prod
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core import db_helper
from core.models.product import Product
from .dependencies import get_product_by_title
from api_v1.shop.schemas import ShopAll, ShopWithId
from api_v1.shop.dependencies import find_shop_depends
from .schemas import ProductCreate, ProductAll, ProductUpdate

router = APIRouter(prefix="/product", tags=["Actions with products"])


# CREATE
@router.post("/", response_model=ProductCreate)
async def craete_product(
    product: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_product(
        session=session,
        product=product,
    )


@router.post("/add_product")
async def add_product_to_shop(
    session: AsyncSession = Depends(db_helper.session_dependency),
    product: ProductAll = Depends(get_product_by_title),
    shop: ShopAll = Depends(find_shop_depends),
):
    return await crud.add_product_to_shop(
        product=product,
        session=session,
        shop=shop,
    )


# READ
@router.get("/", response_model=ProductAll)
async def get_product(
    product: ProductAll = Depends(get_product_by_title),
):
    return product


# UPDATE
@router.patch("/", response_model=ProductAll)
async def update_product(
    update_product: ProductUpdate,
    product: Product = Depends(get_product_by_title),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        update_product=update_product,
    )


# DELETE
@router.delete("/")
async def delete_product(
    session: AsyncSession = Depends(db_helper.session_dependency),
    product: Product = Depends(get_product_by_title),
):
    return await crud.delete_product(product=product, session=session)
