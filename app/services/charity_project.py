from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.investment import Investment
from app.services.validators import (check_charity_project_active,
                                     check_charity_project_exists,
                                     check_charity_project_has_investment,
                                     check_charity_project_updated_amount,
                                     check_name_duplicate)


async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession,
) -> CharityProject:
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    new_project = await Investment.donation_process(new_project, session, Donation)
    return new_project


async def get_charity_projects(
    session: AsyncSession,
) -> list[CharityProject]:
    return await charity_project_crud.get_multi(session)


async def update_charity_project(
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
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_charity_project_has_investment(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project