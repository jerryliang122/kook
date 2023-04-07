import json
import os
from khl import Bot, Message
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from chatglm import chatGLM_Primitive


# 初始化程序
def init_pg():
    global config
    # 检查当前目录下是否含有config.json文件
    if os.path.exists("config.json"):
        # 如果有，则读取文件
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        # 如果没有，则创建文件
        config = {"bot": ""}
        with open("config.json", "w") as f:
            json.dump(config, f)


# 加载bot token
bot = Bot(token=config["bot"])
chatGLM = None
channel = None
history = []


# 获取帮助
@bot.command(name="帮助")
async def help(msg: Message):
    await msg.ctx.channel.send(
        CardMessage(
            Card(
                Module.Header("闲聊机器人的帮助小直男"),
                Module.Context("♂"),
                Module.Section(
                    "使用/chatGLM_Primitive在该频道启用chatGLM。",
                    "使用/clean清除曾经的历史消息",
                    "使用/chatGLM_Fine_tuning在该频道里启用微调后的ChatGLM",
                ),
            )
        )
    )


# 启用chatGLM_Primitive
@bot.command(name="chatGLM_Primitive")
async def chatGLM_Primitive(msg: Message):
    global chatGLM
    global channel
    chatGLM = "Primitive"
    channel = msg.ctx.channel.id
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
    # 如果没有激活频道和chatGLM
    if channel is None and chatGLM is None:
        return
    # 如果激活的频道和消息的频道不一致
    if msg.target_id != msg.ctx.channel.id:
        return
    # 获取原始GLM的回复
    if chatGLM == "Primitive":
        # 构建json请求头
        data = {"prompt": msg.content, "history": history}
        resp = chatGLM_Primitive(data)
        # 将回复和问题组成元组
        history.append((msg.content, resp))
    # 获取微调后的GLM的回复
    elif chatGLM == "Fine_tuning":
        # 构建json请求头
        data = {"prompt": msg.content, "history": history}
        resp = chatGLM_Fine_tuning(data)
        # 将回复和问题组成元组
        history.append((msg.content, resp))
    # 发送回复
    await msg.ctx.channel.send(resp)
