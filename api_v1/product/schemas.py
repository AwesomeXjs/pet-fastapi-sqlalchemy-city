from pydantic import BaseModel, ConfigDict, Field

from core.models.product import ProductTypes
from api_v1.shop.schemas import ShopAll, ShopWithId


class ProductBase(BaseModel):
    title: str = Field(max_length=50)
    type: ProductTypes
    price: int = Field(ge=1)

    # shops: Mapped[list["Shop"]] = relationship(
    #     back_populates="products",
    #     secondary="shop_assotiation_table",
    # )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    title: str | None = None
    type: ProductTypes | None = None
    price: int | None = None


class ProductAll(ProductBase):
    id: int
    shops: list[ShopWithId] | None
    model_config = ConfigDict(from_attributes=True)
