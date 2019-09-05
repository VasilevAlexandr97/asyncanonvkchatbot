import json


class ParserVkRequest:
    def __init__(self, request):
        self.request = request

    # Метод отдает id пользователя
    async def get_user_id(self):
        json = await self.request.json()
        return json['object']['from_id']

    # Метод отдает payload кнопки
    async def get_payload(self):
        jsn = await self.request.json()
        if 'payload' in jsn['object'].keys():
            return json.loads(jsn['object']['payload'])
        else:
            return None

    # Метод отдает текст сообщения
    async def get_message(self):
        json = await self.request.json()
        return json['object']['text']

    # Метод отдает тип запроса
    async def get_type(self):
        json = await self.request.json()
        return json['type']

    async def get_attachment(self):
        try:
            json = await self.request.json()
            return json['object']['attachments'][0]['photo']['sizes'][-1]['url']
        except:
            return ''
