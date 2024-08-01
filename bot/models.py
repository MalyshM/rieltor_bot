import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, \
    String, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)


def async_session_generator():
    return async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def connect_db() -> AsyncSession:
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


class Admins(Base):
    __tablename__ = 'admins'
    __table_args__ = (
        PrimaryKeyConstraint('tg_id', name='admins_pkey'),
    )

    tg_id = mapped_column(BigInteger)
    name = mapped_column(String, nullable=False)
    link = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    date_of_update = mapped_column(DateTime)

    selection: Mapped[List['Selection']] = relationship(
        'Selection', uselist=True, back_populates='admin')
    users: Mapped[List['Users']] = relationship(
        'Users', uselist=True, back_populates='admin')


class Selection(Base):
    __tablename__ = 'selection'
    __table_args__ = (
        ForeignKeyConstraint(['admin_id'], ['admins.tg_id'],
                             ondelete='CASCADE', name='selection_admin_id_fkey'),
        PrimaryKeyConstraint('id', name='selection_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('selection_id_seq'::regclass)"))
    type_of = mapped_column(String, nullable=False)
    link = mapped_column(String, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    admin_id = mapped_column(BigInteger, nullable=False)
    date_of_update = mapped_column(DateTime)

    admin: Mapped['Admins'] = relationship(
        'Admins', back_populates='selection')


class Users(Base):

    def __str__(self):
        attrs = vars(self)
        result_str = ''
        for key, item in attrs.items():
            if key != '_sa_instance_state':
                result_str += f"{key} - {item},\n"
        return result_str

    def __repr__(self):
        return self.__str__()

    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['admin_id'], ['admins.tg_id'],
                             ondelete='CASCADE', name='users_admin_id_fkey'),
        PrimaryKeyConstraint('tg_id', name='users_pkey')
    )

    id = mapped_column(BigInteger, nullable=False, server_default=text(
        "nextval('users_id_seq'::regclass)"))
    name = mapped_column(String, nullable=False)
    tg_id = mapped_column(Integer)
    link = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    admin_id = mapped_column(BigInteger, nullable=False)
    years = mapped_column(String)
    date_of_birth = mapped_column(Date)
    phone_number = mapped_column(String)
    work_phone_number = mapped_column(String)
    salary = mapped_column(Integer)
    place_of_work = mapped_column(String)
    children = mapped_column(String)
    date_of_update = mapped_column(DateTime)

    admin: Mapped['Admins'] = relationship('Admins', back_populates='users')
    buy_request: Mapped[List['BuyRequest']] = relationship(
        'BuyRequest', uselist=True, back_populates='user')
    sell_request: Mapped[List['SellRequest']] = relationship(
        'SellRequest', uselist=True, back_populates='user')
    users_conlultation: Mapped[List['UsersConlultation']] = relationship('UsersConlultation', uselist=True,
                                                                         back_populates='user')
    users_mortgage: Mapped[List['UsersMortgage']] = relationship(
        'UsersMortgage', uselist=True, back_populates='user')
    users_questions: Mapped[List['UsersQuestions']] = relationship('UsersQuestions', uselist=True,
                                                                   back_populates='user')


class BuyRequest(Base):
    __tablename__ = 'buy_request'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.tg_id'],
                             ondelete='CASCADE', name='buy_request_user_id_fkey'),
        PrimaryKeyConstraint('id', name='buy_request_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('buyrequest_id_seq'::regclass)"))
    type_of_object_buy = mapped_column(String, nullable=False)
    cost_range = mapped_column(String, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    user_id = mapped_column(BigInteger, nullable=False)
    type_of_object_buy_detail = mapped_column(String)
    land_square = mapped_column(String)
    number_of_rooms = mapped_column(Integer)
    square = mapped_column(String)
    location_ = mapped_column(String)
    calculation_format = mapped_column(String)
    is_approved = mapped_column(Boolean)

    user: Mapped['Users'] = relationship('Users', back_populates='buy_request')


class SellRequest(Base):
    __tablename__ = 'sell_request'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.tg_id'],
                             ondelete='CASCADE', name='sell_request_user_id_fkey'),
        PrimaryKeyConstraint('id', name='sell_request_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('sellrequest_id_seq'::regclass)"))
    type_of_object = mapped_column(String, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    user_id = mapped_column(BigInteger, nullable=False)
    address = mapped_column(String)
    number_of_rooms = mapped_column(Integer)
    square = mapped_column(String)

    user: Mapped['Users'] = relationship(
        'Users', back_populates='sell_request')


class UsersConlultation(Base):
    __tablename__ = 'users_conlultation'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], [
                             'users.tg_id'], ondelete='CASCADE', name='users_conlultation_user_id_fkey'),
        PrimaryKeyConstraint('id', name='users_conlultation_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('usersconsultation_id_seq'::regclass)"))
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    user_id = mapped_column(BigInteger, nullable=False)

    user: Mapped['Users'] = relationship(
        'Users', back_populates='users_conlultation')


class UsersMortgage(Base):
    __tablename__ = 'users_mortgage'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.tg_id'],
                             ondelete='CASCADE', name='users_mortgage_user_id_fkey'),
        PrimaryKeyConstraint('id', name='users_mortgage_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('usersmortgage_id_seq'::regclass)"))
    family_mortgage = mapped_column(Boolean, nullable=False)
    rural_mortgage = mapped_column(Boolean, nullable=False)
    base_rate = mapped_column(Boolean, nullable=False)
    it_mortgage = mapped_column(Boolean, nullable=False)
    state_support_2020 = mapped_column(Boolean, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    user_id = mapped_column(BigInteger, nullable=False)

    user: Mapped['Users'] = relationship(
        'Users', back_populates='users_mortgage')


class UsersQuestions(Base):
    __tablename__ = 'users_questions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], [
                             'users.tg_id'], ondelete='CASCADE', name='users_questions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='users_questions_pkey')
    )

    id = mapped_column(BigInteger, server_default=text(
        "nextval('usersquestions_id_seq'::regclass)"))
    question = mapped_column(Boolean, nullable=False)
    date_of_add = mapped_column(
        DateTime, nullable=False, default=datetime.now())
    user_id = mapped_column(BigInteger, nullable=False)

    user: Mapped['Users'] = relationship(
        'Users', back_populates='users_questions')
