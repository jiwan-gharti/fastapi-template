from sqlalchemy import Column, String, Float, Text
from sqlalchemy.orm import relationship

from apps.common.model import TimeStampMixin
from apps.config.db.base import Base



class Organization(Base, TimeStampMixin):
    __tablename__ = 'organizations'

    name: str = Column(String(255), unique=True, nullable=False)
    description: str = Column(Text, nullable=True)
    latitude: Float = Column(Float, nullable=True)
    longitude: Float = Column(Float, nullable=True)
    zipcode: str = Column(String, nullable=True)

    # instructor = relationship("User", back_populates="organization", secondary="instructor_organizations")





class School(Base, TimeStampMixin):

    __tablename__ = 'schools'

    name: str = Column(String, unique=True, nullable=False)
    description: str = Column(Text, nullable=False)
    address: str = Column(String, nullable=True)
    latitude: Float = Column(Float, nullable=True)
    longitude: Float = Column(Float, nullable=True)
    zipcode: str = Column(String, nullable=True)





