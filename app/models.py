import os
import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from sqlalchemy import Integer, Float, String, DateTime, func

POSTGRES_DB = os.getenv( "POSTGRES_DB" )
POSTGRES_USER = os.getenv( "POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv( "POSTGRES_PASSWORD" )
POSTGRES_HOST = os.getenv( "POSTGRES_HOST" )
POSTGRES_PORT = os.getenv( "POSTGRES_PORT" )

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine( PG_DSN )

DbSession = async_sessionmaker( bind=engine, expire_on_commit=False )

class Base( DeclarativeBase, AsyncAttrs ):
    pass


class AdsBase( Base ):
    __tablename__ = "ads1_table"

    id: Mapped[int] = mapped_column( Integer, primary_key=True )
    created_at: Mapped[datetime.datetime] = mapped_column( DateTime( timezone=True ), server_default=func.now() )
    title: Mapped[str] = mapped_column( String )
    description: Mapped[str] = mapped_column( String )
    price: Mapped[float] = mapped_column( Float )
    author: Mapped[str] = mapped_column( String )

    def dict(self):
        return { 
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            }

async def init_orm():
    async with engine.begin() as conn:
        # await conn.run_sync( Base.metadata.drop_all ) 
        await conn.run_sync( Base.metadata.create_all )


async def close_orm():
    await engine.dispose()

ORM_OBJ = AdsBase
ORM_CLS = type[AdsBase]