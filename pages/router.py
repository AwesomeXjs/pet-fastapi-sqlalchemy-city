from api_v1.shop.schemas import ShopAll
from core.models.product import Product
from api_v1.product.schemas import ProductAll
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request
from api_v1.product.views import get_all_shops_with_products


router = APIRouter(prefix="/pages", tags=["Pages"])


templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_template(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/shops")
def get_shops_with_prods(
    request: Request, shops: list[ShopAll] = Depends(get_all_shops_with_products)
):
    return templates.TemplateResponse(
        "shops.html", {"request": request, "shops": shops}
    )
