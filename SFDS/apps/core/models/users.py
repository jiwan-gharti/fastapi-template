from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy import Column, Integer, DateTime, BigInteger

from apps.config.db.base import Base
from apps.common.model import TimeStampMixin
from apps.common.enum import GenderEnum
from sqlalchemy import Enum as SQLAlchemyEnum



class Role(Base, TimeStampMixin):
    __tablename__ = 'roles'

    name = Column(String(255))



class Users(Base, TimeStampMixin):

    __tablename__: str = 'users'

    first_name: str = Column(String(50), nullable=False)
    middle_name: str = Column(String(50), nullable=True)
    last_name: str = Column(String(50), nullable=True)
    email: str = Column(String(255), unique=True, index=True)
    password: str = Column(String(255))
    initial_password: str = Column(String(255), nullable=True)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", backref="users")


    school_id = Column(Integer, ForeignKey('schools.id')) # for student
    # school = relationship("School", backref='school_users')
    organization_id = Column(Integer, ForeignKey('organizations.id')) # for Instructor

    # organization = relationship("Organization", back_populates="users", secondary="instructor_organizations")

    # permit_information = relationship("PermitInformation", backref='permit_user', join_depth=2, lazy="joined")
    # contact_information = relationship("ContactInformation", backref='contact_user', join_depth=2, lazy="joined")
    # pickup_location = relationship("PickupLocation", backref='pickup_user', join_depth=2, lazy="joined")



class Profile(Base, TimeStampMixin):
    __tablename__: str = 'user_profiles'

    address: str = Column(String, nullable=True)
    office_note: str = Column(String, nullable=True)
    apartment: str = Column(String, nullable=True)

    city: str = Column(String, nullable=True)
    state: str = Column(String, nullable=True)
    zip_code: str = Column(String, nullable=True)
    dob: datetime = Column(Date, nullable=True)
    gender: datetime = Column(SQLAlchemyEnum(GenderEnum), nullable=True)
    cell_phone: str = Column(BigInteger, nullable=True)



class ContactInformation(Base, TimeStampMixin):
    __tablename__: str = 'user_contact_informations'

    contact_name: str = Column(String(255))
    contact_relationship: str = Column(String(255), nullable=True)
    contact_phone: str = Column(Integer, nullable=True)
    contact_email: str = Column(String, nullable=True)
    contact_type: str = Column(String(255), nullable=True)

    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    users = relationship("Users", backref='user_contacts', foreign_keys=[user_id])

    created_by_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_by = relationship("Users", foreign_keys=[created_by_id])


class PermitInformation(Base, TimeStampMixin):
    __tablename__: str = 'user_permit_informations'

    permit_number: str = Column(String(255))
    permit_issue_date: datetime = Column(DateTime, nullable=True)
    permit_expiration_date: datetime = Column(DateTime, nullable=True)
    permit_endorse_date: datetime = Column(DateTime, nullable=True)

    permit_endorse_by_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    permit_endorse_by = relationship("Users", backref='permit_infomations', join_depth=2, lazy='joined', foreign_keys=[permit_endorse_by_id])

    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    users = relationship("Users", backref='user_permits', foreign_keys=[user_id])

    created_by_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_by = relationship("Users", foreign_keys=[created_by_id])


class PickupLocation(Base, TimeStampMixin):
    __tablename__: str = 'pickup_locations'

    name: str = Column(String(255))
    address: str = Column(String(255), nullable=True)
    apartment: str = Column(String(255), nullable=True)
    city: str = Column(String(255), nullable=True)
    # pickup_location_type = Column(String, nullable=True)

    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    users = relationship("Users", backref='user_pickup_locations', foreign_keys=[user_id])


    created_by_id: int = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_by = relationship("Users", foreign_keys=[created_by_id])



class InstructorOrganization(Base):
    __tablename__: str = 'instructor_organizations'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    instructor_id: int = Column(BigInteger, ForeignKey('users.id'))
    organization_id: int = Column(BigInteger, ForeignKey('organizations.id'))


