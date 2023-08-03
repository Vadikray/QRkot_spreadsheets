from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.error_handlers import (
    NameDuplicateException,
    MissingProjectException,
    EditProjectException,
)
from app.schemas.charity_project import (CharityProjectUpdate)
from app.services.validators import check_charity_project_updated_amount


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if room_id is not None:
        raise NameDuplicateException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise MissingProjectException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого проекта нет!'
        )
    return charity_project


async def check_charity_project_active(
    charity_project: CharityProject,
) -> CharityProject:
    if charity_project.fully_invested:
        raise EditProjectException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await check_charity_project_active(
        charity_project
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if not obj_in.full_amount:
        charity_project = await charity_project_crud.update(
            charity_project, obj_in, session
        )
        return charity_project
    await check_charity_project_updated_amount(
        obj_in.full_amount,
        charity_project.invested_amount,
    )
    return charity_project
