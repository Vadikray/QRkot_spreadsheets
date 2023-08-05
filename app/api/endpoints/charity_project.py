from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.charity_project import (create_charity_project,
                                          delete_charity_project,
                                          get_charity_projects,
                                          update_charity_project)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_defaults=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров."""
    return await create_charity_project(charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
) -> list[CharityProject]:
    return await get_charity_projects(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров."""
    return await update_charity_project(
        charity_project_id=charity_project_id,
        obj_in=obj_in,
        session=session,
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров."""
    return await delete_charity_project(charity_project_id, session)
