import discord
from discord.ext import commands
import os
from discord import Option
from pathlib import Path

import logger

error_color = 0xF1411C
default_color = 0x5FE1EA
base_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = str(Path(__file__).parent.parent.absolute())


class Welcome(commands.cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    @discord.slash_command(name="welcome", description="測試加入訊息", guild_ids=[1172902183205871747,
                                                                            857996539262402570])
    @commands.has_role(1193209412018524180)
    async def welcome(self, ctx, name: Option(str, required=True)):
        embed = discord.Embed(title="歡迎加入", color=0x00ff00)
        embed.add_field(name=f"歡迎{name}加入TFA的大家庭!", value="加入後請先去<#1188142041906036817>領取組別身分組!",
                        inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot, bot.logger))
    bot.logger.info("\"Welcome\"已被載入。")
