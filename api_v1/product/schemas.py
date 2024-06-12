from pydantic import BaseModel, ConfigDict, Field

from core.models.product import ProductTypes


class ProductBase(BaseModel):
    title: str = Field(max_length=50)
    type: ProductTypes
    price: int = Field(ge=1)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    title: str | None = None
    type: ProductTypes | None = None
    price: int | None = None


class ProductAll(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
