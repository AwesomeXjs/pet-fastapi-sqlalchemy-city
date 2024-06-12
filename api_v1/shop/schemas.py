from typing import TYPE_CHECKING

from api_v1.person.schemas import Person
from pydantic import BaseModel, ConfigDict, Field

from api_v1.product.schemas import ProductAll


class ShopBase(BaseModel):
    title: str = Field(max_length=20)
    rating: int | None = None


class CreateShop(ShopBase):
    pass


class UpdateShop(CreateShop):
    title: str | None = None
    products: str | None = None
    rating: int | None = None


class ShopWithId(ShopBase):
    id: int


class ShopWithoutWorkers(ShopWithId):
    model_config = ConfigDict(from_attributes=True)
    products: list[ProductAll]


class ShopAll(ShopWithoutWorkers):

    workers: list[Person]
