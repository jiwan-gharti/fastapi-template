from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.config.db.conn import get_db
from apps.core.models import Profile, PermitInformation, PickupLocation, ContactInformation
from apps.core.schemas.profile import ProfileCreate, ContactInformationCreate, ProfileResponseSchema

router = APIRouter()

@router.post("/profile", response_model=ProfileResponseSchema)
async def profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    db_profile = Profile(
        address=profile.address
    )
    #
    db.add(db_profile)
    db.flush()
    # Create ContactInfomation if provided
    contact_info = None
    if profile.contact_information:
        contact_info = ContactInformation(
            **profile.contact_information.model_dump()
        )
        db.add(contact_info)
        db.flush()

    # Create PickupLocation if provided
    pickup_location = None
    if profile.pickup_location:
        for pickup_location in profile.pickup_location:
            pickup_location = PickupLocation(
                **pickup_location.model_dump(),
                user_id=1
            )
            db.add(pickup_location)
            db.flush()

    # Create PermitInfomation if provided
    permit_info = None
    if profile.permit_information:
        permit_info = PermitInformation(**profile.permit_information.model_dump())
        db.add(permit_info)
        db.flush()

    db.commit()





    # Create Profile

    db.refresh(db_profile)

    return db_profile