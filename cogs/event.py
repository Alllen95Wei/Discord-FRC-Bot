import discord
from discord.ext import commands
from discord import Option
import datetime

import logger
from TBAClient import Event

default_color = 0x012a5e
error_color = 0xF1411C


class EventCmd(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    event = discord.SlashCommandGroup(name="event", description="顯示指定活動的資訊。")

    @event.command(name="what_is_event_key", description="什麼是活動代碼？")
    async def what_is_event_key(self, ctx,
                                私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        embed = discord.Embed(title="什麼是活動代碼？", description="FRC的每場活動，如區域賽等，皆有自己的「活動代碼」。",
                              color=default_color)
        embed.add_field(name="從TBA取得活動代碼",
                        value="在TBA中打開任何一場活動，並查看網址列。\n網址列中的「event/」後面的字串即為該活動的活動代碼。")
        embed.add_field(name="從FRC Events取得活動代碼",
                        value="在FRC Events中打開任何一場活動，並查看網址列。\n網址列中的「...inspires.org/」後面的"
                              "數字為年分，而在數字後方的則為名稱縮寫。\n將年分與名稱縮寫結合，即為該活動的活動代碼。")
        embed.set_image(url="https://media.discordapp.net/attachments/1099274376005816320/1100208334927306852/"
                            "e3bcfb95abc83921.png")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @event.command(name="info", description="Gets information about the event.",
                   description_localizations={"zh-TW": "取得指定活動的資訊。"})
    async def e_info(self, ctx,
                     活動代碼: Option(str, required=True,  # noqa
                                      name="event_key", name_localizations={"zh-TW": "活動代碼"},
                                      description="FRC event key. Use /event what_is_event_key to get help.",
                                      description_localizations={
                                          "zh-TW": "FRC活動代碼。使用/event what_is_event_key指令來取得說明。"}),
                     私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        await ctx.defer()
        m_event = Event(活動代碼)
        try:
            m_event_info = m_event.get_info()
            self.real_logger.debug(m_event_info)
        except ValueError as e:
            embed = discord.Embed(title="錯誤", description="找不到指定的活動。", color=error_color)
            embed.add_field(name="不知道什麼是活動代碼嗎？",
                            value="請使用</event what_is_event_key:1099893824479821934>指令來取得說明。",
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
        embed.add_field(name="地點", value=f"[{m_event_info['location_name']}]({m_event_info['gmaps_url']})",
                        inline=False)
        embed.add_field(name="日期", value=f"<t:{start_date_unix}:D> ~ <t:{end_date_unix}:D> *(時區可能不正確)*",
                        inline=False)
        embed.add_field(name="活動網站", value=m_event_info['website'], inline=False)
        embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @event.command(name="teams", description="Get a list of the teams participating in the event.",
                   description_localizations={"zh-TW": "取得參加該比賽的隊伍清單。"})
    async def e_teams(self, ctx,
                      活動代碼: Option(str, required=True,  # noqa
                                       name="event_key", name_localizations={"zh-TW": "活動代碼"},
                                       description="FRC event key. Use /event what_is_event_key to get help.",
                                       description_localizations={
                                           "zh-TW": "FRC活動代碼。使用/event what_is_event_key指令來取得說明。"}),
                      私人訊息: Option(bool, "是否以私人訊息回應", required=False) = False):  # noqa
        await ctx.defer()
        m_event = Event(活動代碼)
        try:
            m_event_teams = m_event.get_team_list()
            embed = discord.Embed(title=f"活動 {活動代碼} 的參加隊伍",
                                  description=f"參賽的隊伍(共`{len(m_event_teams)}`支)將列於下方。",
                                  url=f"https://www.thebluealliance.com/event/{活動代碼}",
                                  color=default_color)
            embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
            await ctx.respond(embed=embed, ephemeral=私人訊息)
        except ValueError as e:
            embed = discord.Embed(title="錯誤", description="找不到指定的活動。", color=error_color)
            embed.add_field(name="不知道什麼是活動代碼嗎？",
                            value="請使用</event what_is_event_key:1099893824479821934>指令來取得說明。",
                            inline=False)
            embed.add_field(name="錯誤訊息", value=str(e), inline=False)
            await ctx.respond(embed=embed, ephemeral=私人訊息)
            return
        if m_event_teams and len(m_event_teams) <= 25:
            embed = discord.Embed(title=f"活動 {活動代碼} 的參加隊伍(1/1)",
                                  url=f"https://www.thebluealliance.com/event/{活動代碼}",
                                  color=default_color)
            for m_team in m_event_teams:
                team_no = m_team["team_number"]
                team_name = m_team["nickname"]
                team_link = f"https://www.thebluealliance.com/team/{team_no}"
                embed.add_field(name=team_no, value=f"[{team_name}]({team_link})")
            embeds_list = [embed]
        elif m_event_teams and len(m_event_teams) > 25:
            embeds_list = []
            pages_count = int(len(m_event_teams) / 25) + 1
            for i in range(pages_count):
                temp_teams = m_event_teams[:25]
                embed = discord.Embed(title=f"活動 {活動代碼} 的參加隊伍({i + 1}/{pages_count})",
                                      url=f"https://www.thebluealliance.com/event/{活動代碼}",
                                      color=default_color)
                for m_team in temp_teams:
                    team_no = m_team["team_number"]
                    team_name = m_team["nickname"]
                    team_link = f"https://www.thebluealliance.com/team/{team_no}"
                    embed.add_field(name=team_no, value=f"[{team_name}]({team_link})")
                    m_event_teams.remove(m_team)
                embeds_list.append(embed)
        else:
            embed = discord.Embed(title=f"活動 {活動代碼} 的參加隊伍",
                                  url=f"https://www.thebluealliance.com/event/{活動代碼}",
                                  color=error_color)
            embed.add_field(name="沒有找到任何參賽隊伍資料。", value="該活動似乎尚未開放報名或更新。", inline=False)
            embeds_list = [embed]
        for e in embeds_list:
            e.set_footer(text="如要查看更多資訊，請點選隊伍名稱進入TBA。")
            await ctx.channel.send(embed=e)


def setup(bot):
    bot.add_cog(EventCmd(bot, bot.logger))
