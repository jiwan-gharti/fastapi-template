from apps.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine



engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



async_engine = create_async_engine(settings.ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass