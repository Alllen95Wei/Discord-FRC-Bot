import discord
from discord.ext import commands
from discord import Option
import os
from dotenv import load_dotenv
import logging
from colorlog import ColoredFormatter
import json

import TBAClient
from TBAClient import Team

# 機器人
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)
# 常用物件、變數
default_color = 0x012a5e
error_color = 0xF1411C
base_dir = os.path.abspath(os.path.dirname(__file__))
# 載入TOKEN
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))


class CreateLogger:
    def __init__(self):
        super().__init__()
        self.c_logger = self.color_logger()
        self.f_logger = self.file_logger()

    @staticmethod
    def color_logger():
        formatter = ColoredFormatter(
            fmt="%(white)s[%(asctime)s] %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        )

        logger = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        return logger

    @staticmethod
    def file_logger():
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        logger = logging.getLogger()
        handler = logging.FileHandler("logs.log", encoding="utf-8")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        return logger

    def debug(self, message: str):
        self.c_logger.debug(message)
        self.f_logger.debug(message)

    def info(self, message: str):
        self.c_logger.info(message)
        self.f_logger.info(message)

    def warning(self, message: str):
        self.c_logger.warning(message)
        self.f_logger.warning(message)

    def error(self, message: str):
        self.c_logger.error(message)
        self.f_logger.error(message)

    def critical(self, message: str):
        self.c_logger.critical(message)
        self.f_logger.critical(message)


# 建立logger
real_logger = CreateLogger()


async def get_avatar(team_no):
    with open(os.path.join(base_dir, "avatar2022.json"), "r") as f:
        avatar_dict = json.loads(f.read())
    if str(team_no) in avatar_dict:
        return avatar_dict[str(team_no)]
    else:
        m_team_avatar = TBAClient.Team(team_no).get_avatar(2022)
    if m_team_avatar is not None:
        uploaded_avatar = await bot.get_channel(1099274376005816320).send(file=discord.File(m_team_avatar))
        uploaded_avatar_url = uploaded_avatar.attachments[0].url
        with open(os.path.join(base_dir, "avatar2022.json"), "w") as f:
            avatar_dict[team_no] = uploaded_avatar_url
            f.write(json.dumps(avatar_dict))
        os.remove(m_team_avatar)
        return uploaded_avatar_url
    else:
        return "https://media.discordapp.net/attachments/1099274376005816320/1099293468200804433/default_avatar.png"


@bot.event
async def on_ready():
    real_logger.info("機器人準備完成！")
    real_logger.info(f"PING值：{round(bot.latency * 1000)}ms")
    real_logger.info(f"登入身分：{bot.user.name}#{bot.user.discriminator}")
    await bot.change_presence(status=discord.Status.dnd)


@bot.slash_command(name="ping", description="查詢機器人PING值(ms)。")
async def ping(ctx,
               私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):
    embed = discord.Embed(title="PONG!✨", color=default_color)
    embed.add_field(name="PING值", value=f"`{round(bot.latency * 1000)}` ms")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


team = bot.create_group(name="team", description="取得隊伍相關資訊")


@team.command(name="info", description="取得隊伍的基本資料。")
async def info(ctx,
               隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),
               私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):
    await ctx.defer()
    m_team = Team(隊號)
    try:
        m_team_info = m_team.get_info()
    except ValueError as e:
        embed = discord.Embed(title="錯誤", description="找不到指定的隊伍。", color=error_color)
        embed.add_field(name="錯誤訊息", value=str(e))
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        return
    real_logger.debug(m_team_info)
    embed = discord.Embed(title=f"FRC #{隊號} 的基本資料", url=f"https://www.thebluealliance.com/team/{隊號}",
                          color=default_color)
    embed.add_field(name="隊名", value=m_team_info["nickname"], inline=False)
    embed.add_field(name="地區", value=f"{m_team_info['city']}, {m_team_info['country']}, {m_team_info['state_prov']}",
                    inline=False)
    embed.add_field(name="創隊年份", value=m_team_info["rookie_year"], inline=False)
    embed.add_field(name="全名", value=m_team_info["name"], inline=False)
    # 取得網頁
    if m_team_info["website"] is not None:
        embed.add_field(name="官方網站", value=m_team_info["website"], inline=False)
    embed.set_thumbnail(url=await get_avatar(隊號))
    embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


@team.command(name="media", description="取得隊伍的社交媒體連結。")
async def media(ctx,
                隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),
                私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):
    m_team = Team(隊號)
    await ctx.defer()
    try:
        m_team_media = m_team.get_social_media()
    except ValueError as e:
        embed = discord.Embed(title="錯誤", description="找不到指定的隊伍。", color=error_color)
        embed.add_field(name="錯誤訊息", value=str(e))
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        return
    embed = discord.Embed(title=f"FRC #{隊號} 的社交媒體", url=f"https://www.thebluealliance.com/team/{隊號}",
                          color=default_color)
    if m_team_media:
        for i in m_team_media:
            if i["type"] == "facebook-profile":
                embed.add_field(name="Facebook",
                                value=f"[{i['foreign_key']}](https://facebook.com/{i['foreign_key']})",
                                inline=False)
            elif i["type"] == "instagram-profile":
                embed.add_field(name="Instagram",
                                value=f"[{i['foreign_key']}](https://instagram.com/{i['foreign_key']})",
                                inline=False)
            elif i["type"] == "twitter-profile":
                embed.add_field(name="Twitter",
                                value=f"[{i['foreign_key']}](https://twitter.com/{i['foreign_key']})",
                                inline=False)
            elif i["type"] == "youtube-channel":
                embed.add_field(name="YouTube",
                                value=f"[{i['foreign_key']}](https://youtube.com/{i['foreign_key']})",
                                inline=False)
            elif i["type"] == "github-profile":
                embed.add_field(name="GitHub",
                                value=f"[{i['foreign_key']}](https://github.com/{i['foreign_key']})",
                                inline=False)
            elif i["type"] == "twitter-profile":
                embed.add_field(name="Twitter",
                                value=f"[{i['foreign_key']}](https://twitter.com/{i['foreign_key']})",
                                inline=False)
    else:
        embed.add_field(name="沒有找到任何社交媒體資料。", value="該隊伍似乎沒有在TBA上登錄任何社交媒體資料。", inline=False)
    embed.set_thumbnail(url=await get_avatar(隊號))
    embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


@team.command(name="awards", description="取得隊伍曾獲得的獎項。")
async def awards(ctx,
                 隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),
                 私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):
    await ctx.defer()
    m_team = Team(隊號)
    try:
        m_team_awards = m_team.get_awards()
        real_logger.debug(m_team_awards)
    except ValueError as e:
        embed = discord.Embed(title="錯誤", description="找不到指定的隊伍。", color=error_color)
        embed.add_field(name="錯誤訊息", value=str(e))
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        return
    embed = discord.Embed(title=f"FRC #{隊號} 的獎項", url=f"https://www.thebluealliance.com/team/{隊號}/history",
                          color=default_color)
    if m_team_awards:
        for i in m_team_awards:
            text = f"[{i['event_key']}](https://www.thebluealliance.com/event/{i['event_key']})"
            for n in i["recipient_list"]:
                if n["team_key"] == f"frc{隊號}" and n["awardee"] is not None:
                    text += f" ({n['awardee']})"
            embed.add_field(name=i["name"],
                            value=text)
    else:
        embed.add_field(name="沒有找到任何獎項資料。", value="該隊伍似乎尚未獲得任何獎項。", inline=False)
    embed.set_thumbnail(url=await get_avatar(隊號))
    embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


# @bot.slash_command(name="event", description="顯示幫助訊息。")


bot.run(TOKEN)
