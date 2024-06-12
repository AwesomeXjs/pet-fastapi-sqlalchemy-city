from pydantic import BaseModel, ConfigDict, Field, EmailStr


class PersonSchemaBase(BaseModel):
    first_name: str = Field(max_length=10)
    second_name: str = Field(max_length=15)
    years: int = Field(ge=1)
    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=20)
    work_place_name: str


class PersonSchemaCreate(PersonSchemaBase):
    pass


class PersonSchemaUpdate(PersonSchemaCreate):
    pass


class PersonSchemaUpdatePartial(PersonSchemaCreate):
    first_name: str | None = None
    second_name: str | None = None
    years: int | None = None
    username: str | None = None
    email: EmailStr | None = None


class Person(PersonSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
