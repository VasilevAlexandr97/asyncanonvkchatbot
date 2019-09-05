from sqlalchemy import select, and_
from models import user, room

# класс для работы с юзером в базе данных
class UserDatabase:
    # Метод проверяет наличие пользователя в бд
    async def is_user(self, request, vk_id):
        async with request.app['db'].acquire() as conn:
            query = select([user]).where(user.c.vkid == vk_id)
            u = await conn.fetch(query)
            if u:
                return True
            else:
                return False

    # Метод создает пользователя в бд
    async def create_user(self, request, **kwargs):
        async with request.app['db'].acquire() as conn:
            await conn.fetchrow(user.insert().values(kwargs))
        return True

    # метод обновляет данные пользователя
    async def update_user(self, request, vk_id, **kwargs):
        if kwargs:
            async with request.app['db'].acquire() as conn:
                await conn.fetchrow(
                    user.update().where(user.c.vkid == vk_id)
                    .values(kwargs)
                )
            return True
        else:
            return False

    # метод возвращает строку пользователя из бд
    async def get_user(self, request, vk_id):
        async with request.app['db'].acquire() as conn:
            query = select([user]).where(user.c.vkid == vk_id)
            return dict(await conn.fetchrow(query))

    async def get_que(self, request):
        async with request.app['db'].acquire() as conn:
            query = select([room]).where(
                and_(room.c.f_user != None, room.c.s_user != None)
            )
            rooms = len(await conn.fetch(query))
            query = select([room]).where(
                and_(room.c.s_user == None, room.c.find_sex != None, room.c.find_age != None)
            )
            que = len(await conn.fetch(query))
            query = select([room]).where(
                and_(room.c.s_user == None, room.c.find_sex == None, room.c.find_age == None)
            )
            free_que = len(await conn.fetch(query))
            return rooms + que, que, free_que

    async def get_free_room(self, request, age=None, sex=None, user_sex=None):
        if age is None and sex is None:
            async with request.app['db'].acquire() as conn:
                query = select([room]).where(
                    and_(room.c.s_user == None, room.c.find_sex == None, room.c.find_age == None)
                )
                result = await conn.fetchrow(query)
                if result:
                    return dict(result)
                else:
                    return False
        else:
            async with request.app['db'].acquire() as conn:
                query = select([room]).where(
                    and_(room.c.s_user == None, room.c.sex == sex, room.c.find_age == age, room.c.find_sex == user_sex)
                )
                result = await conn.fetchrow(query)
                if result:
                    return dict(result)
                else:
                    return False
    
    async def update_room(self, request, rid, **kwargs):
        if kwargs:
            async with request.app['db'].acquire() as conn:
                await conn.fetchrow(
                    room.update().where(room.c.id == rid)
                    .values(kwargs)
                )
            return True
        else:
            return False
    
    async def create_room(self, request, **kwargs):
        async with request.app['db'].acquire() as conn:
            await conn.fetchrow(room.insert().values(kwargs))
        return True
    

    async def get_room(self, request, rid):
        async with request.app['db'].acquire() as conn:
            query = select([room]).where(room.c.id == rid)
            result = await conn.fetchrow(query)
            if result:
                return dict(result)
            else:
                return False

    async def get_room_user(self, request, vkid):
        async with request.app['db'].acquire() as conn:
            query = select([room]).where(room.c.f_user == vkid)
            result = await conn.fetchrow(query)
            if result:
                return dict(result)
            else:
                return False
    
    
    async def delete_room(self, request, rid):
        async with request.app['db'].acquire() as conn:
            query = room.delete().where(room.c.id == rid)
            await conn.fetchrow(query)
        return True