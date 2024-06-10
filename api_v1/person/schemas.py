from pydantic import BaseModel, ConfigDict, Field, EmailStr


class PersonSchemaBase(BaseModel):
    first_name: str = Field(max_length=10)
    second_name: str = Field(max_length=15)
    years: int = Field(ge=1)
    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=20)


class PersonSchemaCreate(PersonSchemaBase):
    pass


class PersonSchemaUpdate(PersonSchemaCreate):
    pass


class Person(PersonSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
