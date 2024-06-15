from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from . import crud
from core import db_helper
from core.models.product import Product
from .dependencies import get_product_by_title
from api_v1.shop.dependencies import find_shop_depends
from api_v1.shop.schemas import ShopAll, ShopWithoutWorkers
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
@cache(expire=60)
async def get_product(
    product: ProductAll = Depends(get_product_by_title),
):
    return product


@router.get(
    "/by_shop/{title}",
    response_model=list[ProductAll],
)
@cache(expire=60)
async def get_products_by_shop(
    title: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        result = await crud.get_products_by_shop(
            title=title,
            session=session,
        )
        if len(result):
            return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="В Магазине не обнаружены продукты",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Магазин {title} не найден"
        )


@router.get("/all_shops", response_model=list[ShopWithoutWorkers])
async def get_all_shops_with_products(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.get_all_shops_with_all_products(session=session)
    if len(result) > 0:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Магазины с продуктами не найдены",
    )


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
