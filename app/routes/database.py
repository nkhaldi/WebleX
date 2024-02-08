"""Database models and connection."""

from sqlalchemy import Column, Float, ForeignKey, Integer, MetaData, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from routes.config import Config

config = Config()

DATABASE_URL = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

metadata = MetaData()
Base = declarative_base()


class Route(Base):
    """Route model."""

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Добавим название маршрута для удобства
    points = relationship("RoutePoint", back_populates="route")


class RoutePoint(Base):
    """Route point model."""

    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    route = relationship("Route", back_populates="points")


# Create a new AsyncEngine and AsyncSession
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initialize and connect to the database."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Disconnect from the database."""
    await async_engine.dispose()
