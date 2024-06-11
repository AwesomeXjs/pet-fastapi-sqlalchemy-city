from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from . import crud
from core import db_helper


async def find_shop_depends(
    shop_title: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    shop = await crud.find_shop_by_title(session=session, title=shop_title)
    if shop is not None:
        return shop
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"shop with title '{shop_title}' is not found",
    )
