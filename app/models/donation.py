from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __str__(self):
        return (f'Пожертвование на сумму {self.full_amount}, '
                f'из них потрачено {self.invested_amount}')