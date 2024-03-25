from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class ContactInformationBase(BaseModel):
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_relationship: Optional[str] = None
    contact_type: Optional[str] = None

class ContactInformationCreate(ContactInformationBase):
    pass

class ContactInformationResponse(ContactInformationBase):
    id: int



class PermitInformationBase(BaseModel):
    permit_number: Optional[str] = None
    permit_issue_date: Optional[datetime] = None
    permit_expiration_date: Optional[datetime] = None
    permit_endorse_by_id: Optional[int] = None
    permit_endorse_date: Optional[datetime] = None

class PermitInformationCreate(PermitInformationBase):
    pass

class PermitInformationResponse(PermitInformationBase):
    id: int


class PictureInformationBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    apartment: Optional[str] = None
    city: Optional[str] = None

class PickupLocationCreate(PictureInformationBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
class PickupLocationResponse(PictureInformationBase):
    id: int
    user: Optional[UserResponse] = None



class ProfileCreate(BaseModel):
    address: str
    contact_information: Optional[ContactInformationCreate] = None
    pickup_location: Optional[List[PickupLocationCreate]] = []
    permit_information: Optional[PermitInformationCreate] = None

class ProfileResponseSchema(BaseModel):
    id: int
    address: Optional[str] = None
    # contact_information: List[Optional[ContactInfomation]] = []
    permits: Optional[List[PickupLocationResponse]]= []
    # permit_information: List[Optional[PermitInfomationCreate]] = []



