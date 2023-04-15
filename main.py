import json
import os
from khl import Bot, Message
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from chatglm import chatGLM_Primitive


# 获取bot的环境变量
config = os.environ.get("bot")
# 加载bot token
bot = Bot(token=config)
chatGLM = None
channel = None
history = []
activation = {}

# 帮助示例
helps = """
使用/clean清除曾经的历史消息\n
使用/chatGLM_Primitive在该频道启用chatGLM。\n
使用/chatGLM_Fine_tuning在该频道里启用微调后的ChatGLM。
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


# 启用chatGLM_Primitive
@bot.command(name="chatGLM_Primitive")
async def chatGLM_Primitive_activity(msg: Message):
    global chatGLM
    global channel
    global activation
    chatGLM = "Primitive"
    channel = msg.ctx.channel.id
    # 如果激活了chatGLM_Primitive，写入激活列表
    activation.update({msg.ctx.channel.id: "chatGLM_Primitive"})
    await msg.ctx.channel.send("已经激活chatGLM_Primitive")


# 清除历史消息
@bot.command(name="clean")
async def clean(msg: Message):
    global history
    history = []
    await msg.ctx.channel.send("已经清除历史消息")


# 启用chatGLM_Fine_tuning
@bot.command(name="chatGLM_Fine_tuning")
async def chatGLM_Fine_tuning(msg: Message):
    global chatGLM
    global channel
    chatGLM = "Fine_tuning"
    channel = msg.ctx.channel.id
    await msg.ctx.channel.send("已经激活chatGLM_Fine_tuning")


# 监听消息
@bot.on_message()
async def message(msg: Message):
    # 如果消息是以/开头
    if msg.content.startswith("/"):
        return
    # 如果激活的频道和消息的频道不一致
    if not msg.ctx.channel.id in activation.keys():
        return
    # 获取原始GLM的回复
    if activation[msg.ctx.channel.id] == "chatGLM_Primitive":
        # 构建json请求头
        data = {"prompt": msg.content, "history": history}
        resp = await chatGLM_Primitive(data)
        # 将回复和问题组成元组
    # history.append((msg.content, resp))
    # 获取微调后的GLM的回复
    elif chatGLM == "Fine_tuning":
        # 构建json请求头
        data = {"prompt": msg.content, "history": history}
        resp = await chatGLM_Primitive(data)
    # 将回复和问题组成元组
    history.append([msg.content, resp[1]])
    # 发送回复
    await msg.ctx.channel.send(resp[0])


# 运行bot
bot.run()
