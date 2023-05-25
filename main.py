import json
import os
from khl import Bot, Message, MessageTypes
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from chatglm import chatgpt
import io
import asyncio
import datetime
import base64

# 获取bot的环境变量
config = os.environ.get("bot")
# 加载bot token
bot = Bot(token=config)
activity = None
last_access_time = None
channel_id = None
history = []
time_activity = False
# 创建一个 asyncio.Event 对象
stop_event = asyncio.Event()
# 定义一个时间间隔，表示多长时间没有访问后自动关闭
TIMEOUT = 5 * 60  # 5 分钟
# 帮助示例
helps = """
使用/chat开始对话\n
使用/stop删除AI在这个频道的活动\n
注意AI 绘画只支持英文，且不支持中文字符\n
"""


# 配置一个定时器,当长时间没有人发送消息后删除频道ID 并且在该频道中发送消息
async def timer(msg: Message):
    global channel_id, activity, history, time_activity, last_access_time
    while not stop_event.is_set():
        if last_access_time is not None:
            time_since_last_access = (datetime.datetime.now() - last_access_time).total_seconds()
            if time_since_last_access > TIMEOUT:
                ch = await bot.client.fetch_public_channel(channel_id)
                await ch.send("长时间未访问AI，已关闭，激活请使用/help查看指令")
                channel_id = None
                activity = None
                history = []
                time_activity = False
                break
        await asyncio.sleep(5)


# 获取帮助
@bot.command(name="help")
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


# 启动chatglm_lora
@bot.command(name="chat")
async def chatGLM_lora_start(msg: Message):
    # 获取频道id
    global channel_id
    channel_id = msg.ctx.channel.id
    await msg.ctx.channel.send("已启用chatGLM_微调")

# 关闭频道channel_id
@bot.command(name="stop")
async def stop(msg: Message):
    global channel_id, activity, history
    history = []
    activity = None
    channel_id = None
    await msg.ctx.channel.send("已关闭频道")


# 监听频道
@bot.on_message()
async def chat(msg: Message):
    global history, time_activity
    # 判断是否是指令
    if msg.content.startswith("/"):
        return
    # 判断是否为启用chatGLM的频道
    if not msg.ctx.channel.id == channel_id:
        return
    if not time_activity:
        # 启动定时器
        asyncio.create_task(timer(msg))
        time_activity = True
    #访问本地chatglm
    message = msg.content
    chat_model = chatgpt()
    reply = await chat_model.send_message(message)
    if reply[0] == "FAILED":
        await msg.ctx.channel.send("AI出现错误，请重试")
        return
    # 判断是否为图片
    ch = await bot.client.fetch_public_channel(channel_id)
    if bool(reply[3]) is not False:
        # 将base64转换为图片
        image = base64.b64decode(reply[3][0].split(",")[-1])
        # 将图片转换为io流
        image = io.BytesIO(image)
        # 上传到开黑啦
        img_url = await bot.client.create_asset(image)
        await ch.send(img_url, type=MessageTypes.IMG)
    # 判断是否为语音
    if bool(reply[2]) is not False:
        await ch.send('语音功能暂未开放')
    # 判断是否为文本
    if bool(reply[1]) is not False:
        await ch.send(reply[1][0])




# 运行bot
bot.run()
