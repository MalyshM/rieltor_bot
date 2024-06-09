from models import connect_db_users, User, async_session_conn


async def add_user(id: int) -> bool | str:
    async with async_session_conn() as db:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.id_tg ={id}
        """)
        check_user = query.first()
        if check_user is not None:
            await db.close()
            return "Такой пользователь уже есть"
        db.add(User(id_tg=id, balance=0.0))
        await db.commit()
        await db.close()
    return True


async def get_user(id: int):
    async with async_session_conn() as db:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.id_tg ={id}
        """)
        check_user = query.first()
        if check_user is None:
            await db.close()
            return "Такого пользователя нет"
        await db.close()
    return check_user


async def update_user(id: int, balance_change: float) -> bool | str:
    async with async_session_conn() as db:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.id_tg ={id}
        """)
        check_user = query.first()
        if check_user is None:
            await db.close()
            return "Такого пользователя нет"
        await db.execute(f"""
        UPDATE users
        SET balance = balance + {balance_change}
        WHERE id_tg = {id}
        """)
        await db.commit()
        await db.close()
    return True


async def delete_user(id: int) -> bool | str:
    async with async_session_conn() as db:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.id_tg ={id}
        """)
        check_user = query.first()
        if check_user is None:
            await db.close()
            return "Такого пользователя нет"
        await db.execute(f"""
        DELETE FROM users
        WHERE id_tg = {id};
        """)
        await db.commit()
        await db.close()
    return True
