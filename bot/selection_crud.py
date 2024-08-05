from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models import Selection


async def create_selection(session: AsyncSession, data: dict) -> Selection:
    is_created = await session.execute(
        select(Selection).where(Selection.admin_id == data['admin_id'], Selection.type_of == data['type_of']))
    selection = is_created.scalar_one_or_none()
    if selection:
        raise Exception("Selection is already registered")
    selection = Selection()
    selection.type_of = data['type_of']
    selection.link = data['link']
    selection.admin_id = data['admin_id']
    session.add(selection)
    await session.commit()
    return selection


async def get_selection(session: AsyncSession, admin_id: int, type_of: str) -> Selection | str:
    try:
        result = await session.execute(
            select(Selection).where(Selection.admin_id == admin_id, Selection.type_of == type_of))
        return result.scalar_one()
    except NoResultFound:
        return "У данного риелтора нет ссылки для этой категории"


async def get_all_selections(session: AsyncSession) -> List[Selection]:
    result = await session.execute(select(Selection))
    return result.scalars().all()


async def get_all_selections_by_admin(session: AsyncSession, admin_id: int) -> List[dict]:
    result = await session.execute(select(Selection.type_of, Selection.link).where(Selection.admin_id == admin_id))
    res = result.all()
    result_dicts = [row._asdict() for row in res]
    return result_dicts


async def update_selection(session: AsyncSession, admin_id: int, type_of: str, **kwargs) -> Optional[Selection]:
    try:
        selection = await get_selection(session, admin_id, type_of)
        if selection:
            for key, value in kwargs.items():
                setattr(selection, key, value)
            selection.date_of_update = datetime.now()
            await session.commit()
            return selection
        return None
    except Exception as e:
        print(e)
        await session.rollback()
        raise e


async def delete_selection(session: AsyncSession, selection_id: int) -> bool:
    try:
        selection = await get_selection(session, selection_id)
        if selection:
            await session.delete(selection)
            await session.commit()
            return True
        return False
    except Exception as e:
        await session.rollback()
        raise e
