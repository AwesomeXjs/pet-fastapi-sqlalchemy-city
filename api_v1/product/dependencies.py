from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from . import crud
from core import db_helper


async def get_product_by_title(
    title: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    product = await crud.get_product_by_title(title=title, session=session)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Продукт с названием {title} не найден",
    )
