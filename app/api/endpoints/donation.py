from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBFull
from app.services.donation import (create_donation, get_donations,
                                   get_user_donations)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    """Сделать пожертвование."""
    return await create_donation(donation, session, user)


@router.get(
    '/',
    response_model=list[DonationDBFull],
    response_model_exclude_none=True)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[Donation]:
    return await get_donations(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> Donation:
    """Получает список всех пожертвований для текущего пользователя."""
    return await get_user_donations(session, user)