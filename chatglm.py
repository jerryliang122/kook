import aiohttp
import os
import json

backend_url = os.environ.get('http')


class chatgpt():
    async def send_message(self, message):
        async with aiohttp.ClientSession() as session:
            data = {
                "session_id": "chatglm-123",
                "username": "kook",
                "message": message
            }
            async with session.post(str(backend_url), json=data, timeout=300) as response:
                response_text = await response.text()
                try:
                    datas = json.loads(response_text)
                    return datas['result'], datas['message'], datas['voice'], datas['image']
                except json.JSONDecodeError:
                    return None, None, None, None
                
