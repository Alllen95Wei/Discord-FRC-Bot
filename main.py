import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import logger

# 機器人
intents = discord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None)
# 常用物件、變數
base_dir = os.path.abspath(os.path.dirname(__file__))
# 載入TOKEN
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))


# 建立logger
real_logger = logger.CreateLogger()
bot.logger = real_logger


@bot.slash_command(name="reload", description="重新載入所有extension以套用最新變更。(請先使用「/update」)")
@commands.has_role(1193209412018524180)
async def reload(ctx):
    extension_list = list(bot.extensions)
    response_context = "已經重新載入以下extension：\n"
    embed = discord.Embed(title="重新載入", color=0x012a5e)
    for extension in extension_list:
        bot.reload_extension(extension)
        response_context += extension + "\n"
    embed.description = response_context
    await ctx.respond(embed=embed)


bot.load_extensions("cogs.general", "cogs.event", "cogs.team", "cogs.role_giver", "cogs.welcome")
bot.run(TOKEN)
