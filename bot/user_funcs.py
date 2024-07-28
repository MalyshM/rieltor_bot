from typing import Optional

from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from models import *


async def create_user(session: AsyncSession, data: dict) -> Users:
    is_registered = await session.execute(select(Users).where(Users.tg_id == data['id']))
    user = is_registered.scalar_one_or_none()
    if user:
        raise Exception("User is already registered")

    user = Users()
    user.tg_id = data['id']
    user.name = data['name']
    user.link = data['url']
    user.username = data['username']
    try:
        user.admin_id = data['admin_id']
    except:
        user.admin_id = 981942668

    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, user_id: int) -> Optional[Users]:
    try:
        result = await session.execute(select(Users).where(Users.tg_id == user_id))
        return result.scalar_one()
    except NoResultFound:
        return None


async def get_all_users(session: AsyncSession) -> List[Users]:
    result = await session.execute(select(Users))
    return result.scalars().all()


async def update_user(session: AsyncSession, user_id: int, **kwargs) -> Optional[Users]:
    try:
        user = await get_user(session, user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await session.commit()
            return user
        return None
    except Exception as e:
        print(e)
        await session.rollback()
        raise e


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    try:
        user = await get_user(session, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False
    except Exception as e:
        await session.rollback()
        raise e
