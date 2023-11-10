import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from update import kill_running_bot
from platform import system

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("機器人準備完成！指令已清除完畢。")
    print(f"PING值：{round(bot.latency * 1000)}ms")
    print(f"登入身分：{bot.user.name}#{bot.user.discriminator}")
    print("結束工作...")
    kill_running_bot(os.getpid(), system())

load_dotenv("TOKEN.env")
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
