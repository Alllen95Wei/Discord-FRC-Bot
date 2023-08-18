import discord
from discord.ext import commands
from discord import Option
import os
from dotenv import load_dotenv
import logging
from colorlog import ColoredFormatter
import json
import datetime
import time
import git
from platform import system

import TBAClient
from TBAClient import Team, Event
import update as upd

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
    with open(os.path.join(base_dir, "avatar2023.json"), "r") as f:
        avatar_dict = json.loads(f.read())
    if str(team_no) in avatar_dict:
        return avatar_dict[str(team_no)]
    else:
        m_team_avatar = TBAClient.Team(team_no).get_avatar(2023)
    if m_team_avatar is not None:
        uploaded_avatar = await bot.get_channel(1099274376005816320).send(file=discord.File(m_team_avatar))
        uploaded_avatar_url = uploaded_avatar.attachments[0].url
        with open(os.path.join(base_dir, "avatar2023.json"), "w") as f:
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
               私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
    embed = discord.Embed(title="PONG!✨", color=default_color)
    embed.add_field(name="PING值", value=f"`{round(bot.latency * 1000)}` ms")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


@bot.slash_command(name="about", description="提供關於這隻機器人的資訊。")
async def about(ctx,
                私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
    embed = discord.Embed(title="關於", color=default_color)
    embed.set_thumbnail(url=bot.user.display_avatar)
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


@bot.slash_command(name="update", description="更新機器人。")
async def update(ctx,
                 私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
    if ctx.author == bot.get_user(657519721138094080):
        embed = discord.Embed(title="更新中", description="更新流程啟動。", color=default_color)
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        update_event = discord.Activity(type=discord.ActivityType.playing, name="更新中...")
        await bot.change_presence(status=discord.Status.idle, activity=update_event)
        upd.update(os.getpid(), system())
    else:
        embed = discord.Embed(title="錯誤", description="你沒有權限使用此指令。", color=error_color)
        私人訊息 = True  # noqa
        await ctx.respond(embed=embed, ephemeral=私人訊息)


team = bot.create_group(name="team", description="取得隊伍相關資訊")


@team.command(name="info", description="取得隊伍的基本資料。")
async def info(ctx,
               隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),  # noqa
               私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
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
    embed.add_field(name="地區", value=f"{m_team_info['city']}, {m_team_info['state_prov']}, {m_team_info['country']}",
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
                隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),  # noqa
                私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
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
        embed.add_field(name="沒有找到任何社交媒體資料。", value="該隊伍似乎沒有在TBA上登錄任何社交媒體資料。",
                        inline=False)
    embed.set_thumbnail(url=await get_avatar(隊號))
    embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


@team.command(name="awards", description="取得隊伍曾獲得的獎項。")
async def awards(ctx,
                 隊號: Option(int, "指定的FRC隊伍", min_value=1, max_value=9999, required=True),  # noqa
                 私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
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


event = bot.create_group(name="event", description="顯示指定活動的資訊。")


@event.command(name="what_is_event_key", description="什麼是活動代碼？")
async def what_is_event_key(ctx,
                            私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
    embed = discord.Embed(title="什麼是活動代碼？", description="FRC的每場活動，如區域賽等，皆有自己的「活動代碼」。",
                          color=default_color)
    embed.add_field(name="從TBA取得活動代碼", value="在TBA中打開任何一場活動，並查看網址列。\n網址列中的「event/」後面的字串即為該活動的活動代碼。")
    embed.add_field(name="從FRC Events取得活動代碼", value="在FRC Events中打開任何一場活動，並查看網址列。\n網址列中的「...inspires.org/」後面的"
                                                    "數字為年分，而在數字後方的則為名稱縮寫。\n將年分與名稱縮寫結合，即為該活動的活動代碼。")
    embed.set_image(url="https://media.discordapp.net/attachments/1099274376005816320/1100208334927306852/"
                        "e3bcfb95abc83921.png")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


@event.command(name="info", description="取得指定活動的資訊。")
async def e_info(ctx,
                 活動代碼: Option(str, "指定的活動代碼", required=True),  # noqa
                 私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
    await ctx.defer()
    m_event = Event(活動代碼)
    try:
        m_event_info = m_event.get_info()
        real_logger.debug(m_event_info)
    except ValueError as e:
        embed = discord.Embed(title="錯誤", description="找不到指定的活動。", color=error_color)
        embed.add_field(name="不知道什麼是活動代碼嗎？", value="請使用</event what_is_event_key:1099893824479821934>指令來取得說明。",
                        inline=False)
        embed.add_field(name="錯誤訊息", value=str(e), inline=False)
        await ctx.respond(embed=embed, ephemeral=私人訊息)
        return
    embed = discord.Embed(title=f"活動 {活動代碼} 的資訊", url=f"https://www.thebluealliance.com/event/{活動代碼}",
                          color=default_color)
    embed.add_field(name="名稱", value=m_event_info["name"], inline=False)
    embed.add_field(name="類型", value=m_event_info["event_type_string"], inline=False)
    start_date_unix = int(datetime.datetime.timestamp(datetime.datetime.strptime(m_event_info["start_date"],
                                                                                 "%Y-%m-%d")))
    end_date_unix = int(datetime.datetime.timestamp(datetime.datetime.strptime(m_event_info["end_date"],
                                                                               "%Y-%m-%d")))
    embed.add_field(name="地點", value=f"[{m_event_info['location_name']}]({m_event_info['gmaps_url']})", inline=False)
    embed.add_field(name="日期", value=f"<t:{start_date_unix}:D> ~ <t:{end_date_unix}:D> *(時區可能不正確)*", inline=False)
    embed.add_field(name="活動網站", value=m_event_info['website'], inline=False)
    embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
    await ctx.respond(embed=embed, ephemeral=私人訊息)


bot.run(TOKEN)
