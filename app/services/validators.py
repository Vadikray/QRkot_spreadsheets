from http import HTTPStatus

from app.error_handlers import (EditProjectException)
from app.models.charity_project import CharityProject


async def check_charity_project_has_investment(
    charity_project: CharityProject,
) -> None:
    if charity_project.invested_amount:
        raise EditProjectException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_updated_amount(
    obj_in_full_amount: int,
    charity_project_inv_amount: int,
) -> None:
    if obj_in_full_amount < charity_project_inv_amount:
        raise EditProjectException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )
