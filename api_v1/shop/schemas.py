from api_v1.person.schemas import Person
from pydantic import BaseModel, ConfigDict, Field


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


class ShopAll(ShopWithId):
    model_config = ConfigDict(from_attributes=True)
    workers: list[Person]
