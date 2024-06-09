from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy import BigInteger, Column, Float, MetaData, Table, text

metadata = MetaData()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('teacher_id_seq'::regclass)"))
    id_tg = Column(BigInteger, nullable=False)
    balance = Column(Float(53), nullable=False)


DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/users"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_conn = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def connect_db_users() -> AsyncSession:
    async with async_session_conn() as session:
        yield session
