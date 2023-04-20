import aiohttp
import os

# chatGLM的原始版本API的环境变量
chatGLM_Primitive_URL = os.environ.get("chatGLM_Primitive_URL")


# chatGLM的原始版本API
async def chatGLM_Primitive(text):
    # 请在这里填入你的API地址
    url = chatGLM_Primitive_URL
    data = text
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            resp_data = await resp.json()
            return (resp_data["response"], resp_data["history"])
