from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.models import Donation, User
from app.schemas.donation import DonationCreate
from app.services.investment import Investment


async def create_donation(
    donation: DonationCreate,
    session: AsyncSession,
    user: User
) -> Donation:
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await Investment.donation_process(
        new_donation, session
    )
    return new_donation


async def get_donations(
    session: AsyncSession
) -> list[Donation]:
    donations = await donation_crud.get_multi(session)
    return donations


async def get_user_donations(
    session: AsyncSession,
    user: User
) -> Donation:
    donations = await donation_crud.get_all_donations_user(
        session=session, user=user
    )
    return donations
