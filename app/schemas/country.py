from pydantic import BaseModel


class CountryCreate(BaseModel):
    name: str
