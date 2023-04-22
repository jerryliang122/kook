import json
import os
from khl import Bot, Message, MessageTypes
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from chatglm import chatGLM_Primitive, stable_diffusion
import io

# 获取bot的环境变量
config = os.environ.get("bot")
# 加载bot token
bot = Bot(token=config)
activity = None
history = []
# 帮助示例
helps = """
使用/clean清除曾经的历史消息\n
使用/stop删除AI在这个频道的活动\n
使用/chatGLM_Primitive在该频道启用chatGLM。\n
使用/chatGLM_Fine_tuning在该频道里启用微调后的ChatGLM。不适用
使用/stable-diffusion 在该频道里启用AI绘画\n
注意AI 绘画只支持英文，且不支持中文字符\n
"""


# 获取帮助
@bot.command(name="帮助")
async def help(msg: Message):
    await msg.ctx.channel.send(
        CardMessage(
            Card(
                Module.Header("闲聊机器人的帮助小直男"),
                Module.Context("♂"),
                Module.Section(helps),
            )
        )
    )


# 清除历史消息
@bot.command(name="clean")
async def clean(msg: Message):
    global history
    history = []
    await msg.ctx.channel.send("历史消息已清除")


# 启用chatGLM
@bot.command(name="chatGLM_Primitive")
async def chatGLM_Primitive_start(msg: Message):
    # 获取频道id
    global channel_id, activity
    activity = "chatGLM_Primitive"
    channel_id = msg.ctx.channel.id
    await msg.ctx.channel.send("已启用chatGLM_Primitive")


# 启用stable-diffusion
@bot.command(name="stable-diffusion")
async def stable_diffusion_start(msg: Message):
    global channel_id, activity
    activity = "stable-diffusion"
    channel_id = msg.ctx.channel.id
    await msg.ctx.channel.send("已启用stable-diffusion")


# 关闭频道channel_id
@bot.command(name="stop")
async def stop(msg: Message):
    global channel_id, activity
    activity = None
    channel_id = None
    await msg.ctx.channel.send("已关闭频道")


# 监听频道
@bot.on_message()
async def chat(msg: Message):
    global history
    # 判断是否是指令
    if msg.content.startswith("/"):
        return
    # 判断是否为启用chatGLM的频道
    if not msg.ctx.channel.id == channel_id:
        return
    # 判断激活的是哪个模型
    if activity == "chatGLM_Primitive":
        # 获取回复
        data = {"prompt": msg.content, "history": history}
        reply = await chatGLM_Primitive(data)
        # 存档history
        history = reply[1]
        # 发送回复
        await msg.ctx.channel.send(reply[0])
    if activity == "stable-diffusion":
        # 获取回复
        data = {"prompt": msg.content, "history": []}
        reply = await stable_diffusion(data)
        import base64

        # 还原为图片
        img = base64.b64decode(reply)
        # 把还原的图片放置在IO内存空间中
        img = io.BytesIO(img)
        img.seek(0)
        # 上传到开黑啦
        img_url = await bot.client.create_asset(img)
        await msg.ctx.channel.send(img_url, type=MessageTypes.IMG)


# 运行bot
bot.run()
