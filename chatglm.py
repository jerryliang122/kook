import aiohttp


# chatGLM的原始版本API
def chatGLM_Primitive(text):
    # 请在这里填入你的API地址
    url = "https://api.ainize.ai/chatbot/chatGLM"
    data = text
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            resp_data = resp.json()
            return resp_data["text"]
