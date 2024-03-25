

from typing import AsyncGenerator
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session
from apps.config.db.base import async_session_maker, SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


def get_db() -> SessionLocal:
    print("Connecting to database...")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    scoped_factory = scoped_session(SessionLocal)
    session = scoped_factory()
    try:
        yield session
    finally:
        session.close()
        scoped_factory.remove()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
