from collections.abc import Sequence
from typing import Optional

from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from models import *


async def create_admin(session: AsyncSession, data: dict) -> Admins:
    is_registered = await session.execute(select(Admins).where(Admins.tg_id == data['id']))
    admin = is_registered.scalar_one_or_none()
    if admin:
        raise Exception("Admin is already registered")

    admin = Admins()
    admin.tg_id = data['id']
    admin.name = data['name']
    admin.link = data['url']
    admin.email = 'asd'
    admin.username = data['username']
    admin.date_of_add = datetime.now()
    session.add(admin)
    await session.commit()
    return admin


async def get_admin(session: AsyncSession, admin_id: int) -> Optional[Admins]:
    try:
        result = await session.execute(select(Admins).where(Admins.tg_id == admin_id))
        return result.scalar_one()
    except NoResultFound:
        return None


async def get_admin_users(session: AsyncSession, admin_id: int) -> Optional[str]:
    try:
        result = await session.execute(select(Users).where(Users.admin_id == admin_id))
        result = result.scalars().all()
        result_str = ''
        for index, user in enumerate(result):
            result_str = f'{index + 1} user:\n {user.__str__()}'
        return result_str
    except NoResultFound:
        return None


async def get_all_admins(session: AsyncSession) -> List[Admins]:
    result = await session.execute(select(Admins))
    return result.scalars().all()


async def update_admin(session: AsyncSession, admin_id: int, **kwargs) -> Optional[Admins]:
    try:
        admin = await get_admin(session, admin_id)
        if admin:
            for key, value in kwargs.items():
                setattr(admin, key, value)
            admin.date_of_update = datetime.now()
            await session.commit()
            return admin
        return None
    except Exception as e:
        print(e)
        await session.rollback()
        raise e


async def delete_admin(session: AsyncSession, admin_id: int) -> bool:
    try:
        admin = await get_admin(session, admin_id)
        if admin:
            await session.delete(admin)
            await session.commit()
            return True
        return False
    except Exception as e:
        await session.rollback()
        raise e
