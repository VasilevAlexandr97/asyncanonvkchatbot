import aiohttp
import random
import json


class VkApi:
    API_VERSION = '5.92'
    REQUEST_URL = 'https://api.vk.com/method/'
    timeout = 10

    def __init__(self, access_token: str = None):
        # token полученый в настройках сообщества
        self.access_token = access_token

    # Общий метод для отправки запросов к vk api
    async def send_api_request(self, method_name, params, timeout=None):
        if not timeout:
            timeout = self.timeout
        if not params:
            params = {}

        params['access_token'] = self.access_token
        params['v'] = self.API_VERSION

        async with aiohttp.ClientSession() as session:
            response = await session.get(self.REQUEST_URL + method_name, params=params, timeout=timeout)
            return await response.json()

    # Метод для отправки сообщений вк от имени сообщества
    async def message_send(self, **kwargs):
        kwargs['random_id'] = random.randint(-2147483648, 2147483648)
        try:
            return await self.send_api_request('messages.send', params=kwargs)
        except:
            pass

    # Метод составляет кнопки для клавиатуры
    async def keyboard(self, buttons_dict, count_str):
        KEYBOARD = {'one_time': False, 'buttons': []}
        row = 0
        for index, key in enumerate(buttons_dict):
            if index % count_str == 0:
                KEYBOARD['buttons'].insert(row, [{
                    'action': {
                        'type': 'text',
                        'label': key,
                        'payload': json.dumps({"button": f"{buttons_dict[key]['payload']}"})
                    },
                    'color': buttons_dict[key]['color']
                }])
            else:
                KEYBOARD['buttons'][row].append({
                    'action': {
                        'type': 'text',
                        'label': key,
                        'payload': json.dumps({"button": f"{buttons_dict[key]['payload']}"})
                    },
                    'color': buttons_dict[key]['color']
                })
                # row += 1
            
        return json.dumps(KEYBOARD, ensure_ascii=False)
