import aiohttp
import os


# chatGLM的原始版本API的环境变量
chatGLM_Primitive_URL = os.environ.get("chatGLM_Primitive_URL")
# stable-diffusion的API环境变量
stable_diffusion_URL = os.environ.get("stable_diffusion_URL")
# moss的API环境变量
moss_URL = os.environ.get("moss_URL")
# chatGLM_lora_URL
chatGLM_Lora_URL = os.environ.get("chatGLM_Lora_URL")


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


# stable-diffusion的API
async def stable_diffusion(text):
    url = stable_diffusion_URL
    data = text
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, headers=headers) as resp:
                # 获取返回的base64图片
                resp_data = await resp.json()
                return (resp_data["image"], 200)
        except aiohttp.ClientResponseError as e:
            if e.status == 502:
                return ("后端API服务器出现错误，请稍后再试", 502)


# moss的API
async def moss(text):
    # 请在这里填入你的API地址
    url = moss_URL
    data = text
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, headers=headers) as resp:
                resp_data = await resp.json()
                return (resp_data["response"], resp_data["history"])
        except aiohttp.ClientResponseError as e:
            if e.status == 502:
                return ("后端API服务器出现错误，请稍后再试", "")


# clatglm_Lora的API
async def chatglm_lora(text):
    # 请在这里填入你的API地址
    url = chatGLM_Lora_URL
    data = text
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, headers=headers) as resp:
                resp_data = await resp.json()
                return (resp_data["response"], resp_data["history"])
        except aiohttp.ClientResponseError as e:
            if e.status == 502:
                return ("后端API服务器出现错误，请稍后再试", "")
