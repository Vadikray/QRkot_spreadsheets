from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(example=20)
    comment: Optional[str] = Field(example='Комментарий к донату')


class DonationDB(DonationCreate):
    id: int
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDBFull(DonationDB):
    invested_amount: Optional[int]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]
    user_id: Optional[int]
