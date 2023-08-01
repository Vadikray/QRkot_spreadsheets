from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='Фонд №1')
    description: Optional[str] = Field(None, min_length=1, example='Описание фонда')
    full_amount: Optional[PositiveInt] = Field(example=20)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100, example='Фонд №1')
    description: str = Field(..., min_length=1, example='Описание фонда')
    full_amount: PositiveInt = Field(example=20)


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
