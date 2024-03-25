from sqlalchemy import Column, Integer, String, Float, DateTime, func, BigInteger

from apps.common.model import TimeStampMixin
from apps.config.db.base import Base


class Location(Base):
    __tablename__ = 'locations'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())
