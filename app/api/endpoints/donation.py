from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import Donation, User
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationDBFull
)
from app.services.investment import Investment


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
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await Investment.donation_process(
        new_donation, session
    )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBFull],
    response_model_exclude_none=True)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[Donation]:
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> Donation:
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_all_donations_user(
        session=session, user=user
    )
    return donations