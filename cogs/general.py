import discord
from discord.ext import commands
from discord import Option
import os
from pathlib import Path
import git
import time

import logger
import update

default_color = 0x012a5e
error_color = 0xF1411C
base_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = str(Path(__file__).parent.parent.absolute())


class General(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    @discord.slash_command(name="ping", description="Gets bot's latency in ms.",
                           description_localizations={"zh-TW": "取得機器人的延遲。"})
    async def ping(self, ctx,
                   私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        embed = discord.Embed(title="PONG!✨", color=default_color)
        embed.add_field(name="PING值", value=f"`{round(self.bot.latency * 1000)}` ms")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @discord.slash_command(name="about", description="Provides information about this robot.",
                           description_localizations={"zh-TW": "提供關於這隻機器人的資訊。"})
    async def about(self, ctx,
                    私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        embed = discord.Embed(title="關於", color=default_color)
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(name="程式碼與授權", value="本機器人由<@657519721138094080>維護，使用[Py-cord]"
                                             "(https://github.com/Pycord-Development/pycord)、"
                                             "[TBA](https://www.thebluealliance.com/apidocs/v3)、"
                                             "[FRC API](https://frc-api-docs.firstinspires.org/)進行開發。\n"
                                             "本機器人的程式碼及檔案皆可在[這裡](https://github.com/Alllen95Wei/"
                                             "Discord-FRC-Bot)查看。",
                        inline=True)
        embed.add_field(name="聯絡", value="如果有任何技術問題及建議，請聯絡<@657519721138094080>。", inline=True)
        repo = git.Repo(search_parent_directories=True)
        update_msg = repo.head.reference.commit.message
        raw_sha = repo.head.object.hexsha
        sha = raw_sha[:7]
        embed.add_field(name=f"分支訊息：{sha}", value=update_msg, inline=False)
        year = time.strftime("%Y")
        embed.set_footer(text=f"©Allen Why, {year} | 版本：commit {sha[:7]}")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @discord.slash_command(name="update", description="更新機器人。")
    @commands.has_role(1193209412018524180)
    async def update(self, ctx,
                     私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        embed = discord.Embed(title="更新中", description="更新流程啟動。", color=default_color)
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        update.get_update_files()


class Event(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.real_logger.info("機器人準備完成！")
        self.real_logger.info(f"PING值：{round(self.bot.latency * 1000)}ms")
        self.real_logger.info(f"登入身分：{self.bot.user.name}#{self.bot.user.discriminator}")
        activity = discord.Activity(type=discord.ActivityType.watching, name="FRC")
        await self.bot.change_presence(activity=activity)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="指令冷卻中",
                                  description=f"這個指令正在冷卻中，請在`{round(error.retry_after)}`秒後再試。",
                                  color=error_color)
            await ctx.respond(embed=embed, ephemeral=True)
        elif (isinstance(error, commands.NotOwner) or isinstance(error, commands.MissingRole) or
              isinstance(error, commands.MissingPermissions)):
            embed = discord.Embed(title="錯誤", description="你沒有權限使用此指令。", color=error_color)
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            raise error


def setup(bot):
    bot.add_cog(General(bot, bot.logger))
    bot.logger.info("\"General\"已被載入。")
    bot.add_cog(Event(bot, bot.logger))
    bot.logger.info("\"Event\"已被載入。")
