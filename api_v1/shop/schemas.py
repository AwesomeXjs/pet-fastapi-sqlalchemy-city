from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    title: str = Field(max_length=20)
    products: str
    rating: int | None = None


class CreateShop(ShopBase):
    pass


class UpdateShop(CreateShop):
    title: str | None = None
    products: str | None = None
    rating: int | None = None


class Shop(ShopBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
