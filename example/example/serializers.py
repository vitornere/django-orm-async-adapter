from pydantic import BaseModel


class ExampleCreateUpdateSerializer(BaseModel):
    name: str
    description: str

    # ORM Mode
    class Config:
        orm_mode = True


class ExampleSerializer(ExampleCreateUpdateSerializer):
    id: int
