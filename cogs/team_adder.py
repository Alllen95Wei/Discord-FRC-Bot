import discord
from discord.ext import commands
import os
import json
from pathlib import Path

import logger

error_color = 0xF1411C
default_color = 0x012a5e
base_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = str(Path(__file__).parent.parent.absolute())

with open("config.json", mode="w+") as jdata:
    jdata_setting = json.load(jdata)

class TeamAddCmd(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger
        
    @commands.command()
    async def newteam(ctx, team, id):
        if team in jdata_setting["team"]:
            if id in jdata_setting["team"].values():
                await ctx.respond("此隊伍已新增")
            else:
                await ctx.respond(f"已有此隊伍，但身分組id為{jdata_setting['team'][team]}")
        if id in jdata_setting["team"].values():
            await ctx.respond(f"id已被使用，但隊伍號碼非{team}。請確認{team}對應的id是否是{id}")
        else:
            jdata_setting["team"][team] = id
            with open('config.json', mode='w', encoding='utf8') as jfile:
                json.dump(jdata_setting, jfile)