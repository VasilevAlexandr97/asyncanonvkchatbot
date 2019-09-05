from database import UserDatabase
from vkapi import VkApi
from urlextract import URLExtract
import datetime

EX = URLExtract()
with open('antimat.txt', 'r') as file:
    ANTIMAT = file.read().split(' \n')


async def get_buttons(name, vkid="", f=None):
    if name == 'main':
        buttons = {
            'Поиск по возрасту': {
                'payload': '/select-age',
                'color': 'positive'
            },
            'Случайный собеседник': {
                'payload': '/search',
                'color': 'secondary'
            },
        }
    elif name == "dialog":
        buttons = {
            'Отключить': {
                'payload': '/cancel-dialog',
                'color': 'negative'
            },
            'Следующий собеседник': {
                'payload': '/next',
                'color': 'primary'
            },
        }    
    elif name == "cancel":
        buttons = {
            'Остановить': {
                'payload': '/cancel',
                'color': 'negative'
            }
        }
    elif name == 'select_age':
         buttons = {
            '16-17': {
                'payload': '/select-age:16-17',
                'color': 'primary'
            },
            '18-21': {
                'payload': '/select-age:18-21',
                'color': 'primary'
            },
            '22-25': {
                'payload': '/select-age:22-25',
                'color': 'primary'
            },
            '26+': {
                'payload': '/select-age:26+',
                'color': 'primary'
            }
        }
    elif name == 'select_sex':
        buttons = {
            'Парень': {
                'payload': '/select-sex:boy',
                'color': 'primary'
            },
            'Девушка': {
                'payload': '/select-sex:girl',
                'color': 'positive'
            },
        }
    elif name == 'set_reputation':
        buttons = {
            '1': {
                'payload': f'/set-reputation:1:{vkid}',
                'color': 'primary'
            },
            '2': {
                'payload': f'/set-reputation:2:{vkid}',
                'color': 'primary',
            },
            '3': {
                'payload': f'/set-reputation:3:{vkid}',
                'color': 'primary'
            },
            '4': {
                'payload': f'/set-reputation:4:{vkid}',
                'color': 'primary'
            },
        }
    elif name == 'confirm':
        buttons = {
            'Да': {
                'payload': f'/confirm:yes:{f}',
                'color': 'primary'
                
            },
            'Нет': {
                'payload': f'/confirm:no:{f}',
                'color': 'primary'
            },
        }
    return buttons

async def standart_message(vkid, vkapi, name, reputation, count_people, type_message=0):
    GROUP_LINK = "vk.com/likenvkz"
    group_id = '60449152'
    sub = await vkapi.send_api_request('groups.isMember', {'group_id': group_id, 'user_id': vkid})
    if type_message == 0:
        if sub == 0:
            message = (
                f"Привет {name}!\n\n"
                "В чате запрещены:\n"
                "- спам, оскорбления\n"
                "- реклама и продажа любых услуг\n\n"
                "При нарушении правил пользователь блокируется без предупреждения\n\n"
                f"Советуем подписаться {GROUP_LINK}\n\n"
                f'&#128309; Сейчас в чате {count_people} человек. Выберите возраст или нажмите кнопку "Случайный собеседник"\n\n'
                f'Репутация: {reputation} ⭐'
            )
        else:
            message = (
                f"Привет {name}!\n\n"
                "В чате запрещены:\n"
                "- спам, оскорбления\n"
                "- реклама и продажа любых услуг\n\n"
                "При нарушении правил пользователь блокируется без предупреждения\n\n"
                f'&#128309; Сейчас в чате {count_people} человек. Выберите возраст или нажмите кнопку "Случайный собеседник"\n\n'
                f'Репутация: {reputation} ⭐'
            )
    else:
        if sub == 0:
            message = (
                f"Советуем подписаться {GROUP_LINK}\n\n"
                f'&#128309; Сейчас в чате {count_people} человек. Выберите возраст или нажмите кнопку "Случайный собеседник"\n\n'
                f'Репутация: {reputation} ⭐'
            )
        else:
            message = (
                f'&#128309; Сейчас в чате {count_people} человек. Выберите возраст или нажмите кнопку "Случайный собеседник"\n\n'
                f'Репутация: {reputation} ⭐'
            )
    return message

async def get_info_user(vkapi, vkid):
    result = await vkapi.send_api_request('users.get', {'user_ids': vkid, 'fields': 'sex'})
    if result['response'][0]['sex'] == 1:
        find_sex = 'Найдена девушка'
        sex = 'girl'
    else:
        find_sex = 'Найден парень'
        sex = 'boy'
    return result['response'][0]['first_name'], find_sex, sex


async def get_sex(sex):
    if sex == 'boy':
        find_sex = 'Найден парень'
    else:
        find_sex = 'Найдена девушка'
    return find_sex

async def search(user, db, request, vkapi):
    if user['age'] is None and user['find_sex'] is None:
        room = await db.get_free_room(request)
        if room:
            if user['vkid'] == room['f_user']:
                return
            await db.update_room(request, room['id'], s_user=user['vkid'], first_message_time=datetime.datetime.now())
            await db.update_user(request, user['vkid'], state='dialog', room=room['id'])
            await db.update_user(request, room['f_user'], state='dialog', room=room['id'])
            user_sex = await get_sex(user['sex'])
            user_reputation = user['reputation']
            comp_sex = await get_sex(room['sex'])
            comp_reputation = room['reputation']
            buttons = await get_buttons('dialog')
            await vkapi.message_send(user_id=user['vkid'], message=f'{comp_sex}, можете общаться 📩\n• Репутация: {comp_reputation} ⭐', keyboard=await vkapi.keyboard(buttons, 1))
            await vkapi.message_send(user_id=room['f_user'], message=f'{user_sex}, можете общаться 📩\n• Репутация: {user_reputation} ⭐', keyboard=await vkapi.keyboard(buttons, 1))
        else:
            await db.create_room(request, 
                f_user=user['vkid'],
                sex=user['sex'],
                reputation=user['reputation']
            )
            buttons = await get_buttons('cancel')
            count_people, que, fque = await db.get_que(request)
            await vkapi.message_send(user_id=user['vkid'], message=f'Ищем собеседника... 📢\n\n• Ты находишься в конце очереди\nПеред тобой {fque - 1} человек', keyboard=await vkapi.keyboard(buttons, 1))
    else:
        room = await db.get_free_room(request, age=user['age'], sex=user['find_sex'], user_sex=user['sex'])
        if room:
            if user['vkid'] == room['f_user']:
                return
            await db.update_room(request, room['id'], s_user=user['vkid'], first_message_time=datetime.datetime.now())
            await db.update_user(request, user['vkid'], state='dialog', room=room['id'])
            await db.update_user(request, room['f_user'], state='dialog', room=room['id'])
            user_sex = await get_sex(user['sex'])
            user_reputation = user['reputation']
            comp_sex = await get_sex(room['sex'])
            comp_reputation = room['reputation']
            buttons = await get_buttons('dialog')
            await vkapi.message_send(user_id=user['vkid'], message=f'{comp_sex}, можете общаться 📩\n• Репутация: {comp_reputation} ⭐', keyboard=await vkapi.keyboard(buttons, 1))
            await vkapi.message_send(user_id=room['f_user'], message=f'{user_sex}, можете общаться 📩\n• Репутация: {user_reputation} ⭐', keyboard=await vkapi.keyboard(buttons, 1))
        else:
            await db.create_room(request, 
                f_user=user['vkid'],
                sex=user['sex'],
                reputation=user['reputation'],
                find_sex=user['find_sex'],
                find_age=user['age'],
            )
            buttons = await get_buttons('cancel')
            count_people, que, fque = await db.get_que(request)
            await vkapi.message_send(user_id=user['vkid'], message=f'Ищем собеседника... 📢\n\n• Ты находишься в конце очереди\nПеред тобой {que - 1} человек', keyboard=await vkapi.keyboard(buttons, 1))

async def antimat(text):
    for mat in ANTIMAT:
        text = text.replace(mat.replace(' ', ''), 'xxx')
    return text


async def dialog(user, request, db, vkapi, text, attachment):
    urls = EX.find_urls(text)
    for url in urls:
        text = text.replace(url, 'ссылка')
    room = await db.get_room(request, user['room'])
    if not room:
        return
    if room['f_user'] == user['vkid']:
        companion = room['s_user']
    else:
        companion = room['f_user']
    
    await db.update_room(request, room['id'], last_message_time=datetime.datetime.now())
    text = await antimat(text)
    name = user['name']
    buttons = await get_buttons('dialog')
    await vkapi.message_send(user_id=companion, message=f'💬 {name}:\n{text}{attachment}', keyboard=await vkapi.keyboard(buttons, 1))


async def cancel(user, request, db, vkapi):
    await db.update_user(request, user['vkid'],
        age=None,
        find_sex=None,
    )
    room = await db.get_room_user(request, user['vkid'])
    await db.delete_room(request, room['id'])
    count_people, que, fque = await db.get_que(request)
    message = await standart_message(user['vkid'], vkapi, user['name'], 0, count_people, type_message=1)
    buttons = await get_buttons('main')
    await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 1))

# Вложения

async def confirm(user, vkapi, f):
    message = 'Вы уверены?'
    buttons = await get_buttons('confirm', f=f)
    await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 2))


async def delta_time(room):
    if (datetime.datetime.now() - room['first_message_time']).seconds / 60 > 5:
        return True
    else:
        return False

async def set_reputation(user, request, db, vkapi, vkid=None , ball=None, b=0):
    room = await db.get_room(request, user['room'])
    if b == 0:    
        if room['f_user'] == user['vkid']:
            companion = room['s_user']
        else:
            companion = room['f_user']
        buttons = await get_buttons('set_reputation', vkid=companion)
        await vkapi.message_send(user_id=user['vkid'], message='⚠Собеседник отключён\n\nПоставьте оценку вашему собеседнику ⭐', keyboard=await vkapi.keyboard(buttons, 4))
        buttons = await get_buttons('set_reputation', vkid=user['vkid'])
        await vkapi.message_send(user_id=companion, message='⛔ Твой собеседник отключился\n\nПоставьте оценку вашему собеседнику ⭐', keyboard=await vkapi.keyboard(buttons, 4))
    else:
        count_people, que, fque = await db.get_que(request)
        buttons = await get_buttons('main')
        user_c = await db.get_user(request, int(vkid))
        count_rep = user_c['count_rep'] + 1
        full_rep = user_c['full_rep'] + int(ball)
        reputation = round(full_rep / count_rep, 1)
        await db.update_user(request, int(vkid), count_rep=count_rep, full_rep=full_rep, reputation=reputation)
        message = await standart_message(user['vkid'], vkapi, user['name'], user['reputation'], count_people)
        await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 1))
    
async def cancel_dialog(user, request, db, vkapi, f=''):
    room = await db.get_room(request, user['room'])
    if not room:
        return
    companion = None
    if room['f_user'] == user['vkid']:
        companion = room['s_user']
    else:
        companion = room['f_user']
    if await delta_time(room):
        await set_reputation(user, request, db, vkapi)
    else:
        buttons = await get_buttons('main')
        count_people, que, fque = await db.get_que(request)
        message = '⚠Собеседник отключён\n\n'
        message += await standart_message(user['vkid'], vkapi, user['name'], user['reputation'], count_people, type_message=2)
        await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 1))
        user_c = await db.get_user(request, companion)
        message = '⛔ Твой собеседник отключился\n\n'
        message += await standart_message(user_c['vkid'], vkapi, user_c['name'], user_c['reputation'], count_people, type_message=2)
        await vkapi.message_send(user_id=companion, message=message, keyboard=await vkapi.keyboard(buttons, 1))
    if f == 'next':
        await db.update_user(request, user['vkid'], state=None, room=None)
        await db.update_user(request, companion, state=None, room=None)
        await db.delete_room(request, room['id'])
        await search(user, db, request, vkapi)
    else:
        await db.update_user(request, user['vkid'], state=None, room=None, age=None, find_sex=None)
        await db.update_user(request, companion, state=None, room=None, age=None, find_sex=None)
        await db.delete_room(request, room['id'])


async def select_age(user, request, vkapi, db, age=None):
    if age is None:
        buttons = await get_buttons('select_age')
        message = "Выбери возраст собеседника"
        await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 4))
    else:
        buttons = await get_buttons('select_sex')
        message = "Выбери пол собеседника"
        await db.update_user(request, user['vkid'], age=age)
        await vkapi.message_send(user_id=user['vkid'], message=message, keyboard=await vkapi.keyboard(buttons, 2))


async def select_sex(user, request, vkapi, db, sex):
    await db.update_user(request, user['vkid'], find_sex=sex)
    user = await db.get_user(request, user['vkid'])
    await search(user, db, request, vkapi)


async def commands(user, payload, db, request, vkapi, message, attachment):
    if payload is not None:
        payload = payload['button']
    else:
        payload = ''  
    if payload == '/next':
        await confirm(user, vkapi, 'next')
    elif payload == '/cancel':
        await confirm(user, vkapi, 'cancel')
    elif payload == '/cancel-dialog':
        await confirm(user, vkapi, 'cancel_dialog')
    elif '/confirm' in payload:
        conf = payload.split(':')[1]
        payload = payload.split(':')[2]
        if conf == 'yes':
            if payload == 'cancel':
                await cancel(user, request, db, vkapi)
            elif payload == 'next':
                await cancel_dialog(user, request, db, vkapi, f='next')
            elif payload == 'cancel_dialog':
                await cancel_dialog(user, request, db, vkapi)
        else:
            if payload == 'cancel_dialog' or payload == 'next':
                buttons = await get_buttons('dialog')
                await vkapi.message_send(user_id=user['vkid'], message='Отмена', keyboard=await vkapi.keyboard(buttons, 1))
            else:
                buttons = await get_buttons('cancel')
                await vkapi.message_send(user_id=user['vkid'], message='Отмена', keyboard=await vkapi.keyboard(buttons, 1))
    elif '/set-reputation' in payload:
        ball = payload.split(':')[1]
        vkid = payload.split(':')[2]
        await set_reputation(user, request, db, vkapi, vkid, ball, b=1)
    elif user['state'] == 'dialog':
        await dialog(user, request, db, vkapi, message, attachment)
    elif message.lower() == 'привет' or message.lower() == 'начать':
        count_people, que, fque = await db.get_que(request)
        buttons = await get_buttons('main')
        message = await standart_message(user['vkid'], vkapi, user['name'], user['reputation'], count_people)
        await vkapi.message_send(user_id=user['vkid'], message=message, keyboard= await vkapi.keyboard(buttons, 1))
    elif payload == '/search' or payload == '/age-search':
        await search(user, db, request, vkapi)
    elif payload == '/select-age':
        await select_age(user, request, vkapi, db)
    elif '/select-age' in payload:
        age = payload.split(':')[1]
        await select_age(user, request, vkapi, db, age=age)
    elif '/select-sex' in payload:
        sex = payload.split(':')[1]
        await select_sex(user, request, vkapi, db, sex)
    
                


async def bot(request, vkid, payload, message, attachment):
    db = UserDatabase()
    vk_api = VkApi('Token')
    user = await db.is_user(request, vkid)
    user_info = await get_info_user(vk_api, vkid)
    if user:
        user = await db.get_user(request, vkid)
        await commands(user, payload, db, request, vk_api, message, attachment)
    else:
        count_people, que, fque = await db.get_que(request)
        message = await standart_message(vkid, vk_api, user_info[0], 0, count_people)
        await db.create_user(request, vkid=vkid, sex=user_info[2], name=user_info[0])
        buttons = await get_buttons('main')
        await vk_api.message_send(user_id=vkid, message=message, keyboard=await vk_api.keyboard(buttons, 1))