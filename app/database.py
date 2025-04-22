from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import db_settings

DATABASE_URL = db_settings.DB_URL

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# base class for elements that has created_at and updated_at fields
class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


# generate asynchronous session to database -> easy to use instead of creating new session everytime
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session

# class SessionContextManager:
#
#     def __init__(self) -> None:
#         self.session_factory = async_session_maker
#         self.session = None
#
#     async def __aenter__(self) -> None:
#         self.session = self.session_factory()
#
#     async def __aexit__(self, *args: object) -> None:
#         await self.rollback()
#
#     async def commit(self) -> None:
#         await self.session.commit()
#         await self.session.close()
#         self.session = None
#
#     async def rollback(self) -> None:
#         await self.session.rollback()
#         await self.session.close()
#         self.session = None