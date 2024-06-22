import discord
from discord.ext import commands
from discord import Option
import json
import os
from pathlib import Path
from math import ceil

import logger
from TBAClient import Team

default_color = 0x012a5e
error_color = 0xF1411C
base_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = str(Path(__file__).parent.parent.absolute())


class TeamCmd(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    async def get_avatar(self, team_no):
        with open(os.path.join(parent_dir, "avatar2023.json"), "r") as f:
            avatar_dict = json.loads(f.read())
        if str(team_no) in avatar_dict:
            return avatar_dict[str(team_no)]
        else:
            m_team_avatar = Team(team_no).get_avatar(2023)
        if m_team_avatar is not None:
            uploaded_avatar = await self.bot.get_channel(1099274376005816320).send(file=discord.File(m_team_avatar))
            uploaded_avatar_url = uploaded_avatar.attachments[0].url
            uploaded_avatar_url = uploaded_avatar_url[:uploaded_avatar_url.find("?")]
            with open(os.path.join(parent_dir, "avatar2023.json"), "w") as f:
                avatar_dict[team_no] = uploaded_avatar_url
                f.write(json.dumps(avatar_dict))
            os.remove(m_team_avatar)
            return uploaded_avatar_url
        else:
            return "https://media.discordapp.net/attachments/1099274376005816320/1099293468200804433/default_avatar.png"

    team = discord.SlashCommandGroup(name="team", description="Gets information about the team.",
                                     description_localizations={"zh-TW": "取得隊伍相關資訊。"})

    @team.command(name="info", description="Gets basic information about the team.",
                  description_localizations={"zh-TW": "取得隊伍的基本資料。"})
    async def info(self, ctx,
                   隊號: Option(int, min_value=1, required=True,  # noqa
                                name="team_no", name_localizations={"zh-TW": "隊號"},
                                description="FRC team no.", description_localizations={"zh-TW": "FRC隊伍編號"}),
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
        self.real_logger.debug(m_team_info)
        embed = discord.Embed(title=f"FRC #{隊號} 的基本資料", url=f"https://www.thebluealliance.com/team/{隊號}",
                              color=default_color)
        embed.add_field(name="隊名", value=m_team_info["nickname"], inline=False)
        embed.add_field(name="地區",
                        value=f"{m_team_info['city']}, {m_team_info['state_prov']}, {m_team_info['country']}",
                        inline=False)
        embed.add_field(name="創隊年份", value=m_team_info["rookie_year"], inline=False)
        events = m_team.get_attended_event_keys()
        if events:
            last_event = m_team.get_attended_event_keys()[-1]
            last_active_year = last_event[:4]
            embed.add_field(name="最後活躍年份", value=f"{last_active_year} "
                                                 f"([{last_event}]"
                                                 f"(https://www.thebluealliance.com/event/{last_event}))",
                            inline=False)
        embed.add_field(name="贊助商", value=m_team_info["name"], inline=False)
        # 取得網頁
        if m_team_info["website"] is not None:
            embed.add_field(name="官方網站", value=m_team_info["website"], inline=False)
        embed.set_thumbnail(url=await self.get_avatar(隊號))
        embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @team.command(name="media", description="Gets social media links of the team.",
                  description_localizations={"zh-TW": "取得隊伍的社交媒體連結。"})
    async def media(self, ctx,
                    隊號: Option(int, min_value=1, required=True,  # noqa
                                 name="team_no", name_localizations={"zh-TW": "隊號"},
                                 description="FRC team no.", description_localizations={"zh-TW": "FRC隊伍編號"}),
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
                    embed.add_field(name="<:FB:1168913758228332564>Facebook",
                                    value=f"[{i['foreign_key']}](https://facebook.com/{i['foreign_key']})",
                                    inline=False)
                elif i["type"] == "instagram-profile":
                    embed.add_field(name="<:IG:1168914317505204254>Instagram",
                                    value=f"[{i['foreign_key']}](https://instagram.com/{i['foreign_key']})",
                                    inline=False)
                elif i["type"] == "twitter-profile":
                    embed.add_field(name="<:X_:1169059751695503490>Twitter (X)",
                                    value=f"[{i['foreign_key']}](https://twitter.com/{i['foreign_key']})",
                                    inline=False)
                elif i["type"] == "youtube-channel":
                    embed.add_field(name="<:YT:1168914645466222643>YouTube",
                                    value=f"[{i['foreign_key']}](https://youtube.com/{i['foreign_key']})",
                                    inline=False)
                elif i["type"] == "github-profile":
                    embed.add_field(name="<:GitHub:1169059505301094431>GitHub",
                                    value=f"[{i['foreign_key']}](https://github.com/{i['foreign_key']})",
                                    inline=False)
                else:
                    embed.add_field(name=f"其它({i['type']})", value=i["foreign_key"], inline=False)
        else:
            embed.add_field(name="沒有找到任何社交媒體資料。", value="該隊伍似乎沒有在TBA上登錄任何社交媒體資料。",
                            inline=False)
        embed.set_thumbnail(url=await self.get_avatar(隊號))
        embed.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
        await ctx.respond(embed=embed, ephemeral=私人訊息)

    @team.command(name="awards", description="取得隊伍曾獲得的獎項。")
    async def awards(self, ctx,
                     隊號: Option(int, min_value=1, required=True,  # noqa
                                  name="team_no", name_localizations={"zh-TW": "隊號"},
                                  description="FRC team no.", description_localizations={"zh-TW": "FRC隊伍編號"})):
        await ctx.defer()
        m_team = Team(隊號)
        avatar = await self.get_avatar(隊號)
        try:
            m_team_awards = m_team.get_awards()
            self.real_logger.debug(m_team_awards)
            embed = discord.Embed(title=f"FRC #{隊號} 的獎項",
                                  url=f"https://www.thebluealliance.com/team/{隊號}/history",
                                  description="隊伍的獎項將列於下方。", color=default_color)
            embed.set_thumbnail(url=avatar)
            await ctx.respond(embed=embed)
        except ValueError as e:
            embed = discord.Embed(title="錯誤", description="找不到指定的隊伍。", color=error_color)
            embed.add_field(name="錯誤訊息", value=str(e))
            await ctx.respond(embed=embed)
            return
        if m_team_awards and len(m_team_awards) <= 25:
            embed = discord.Embed(title=f"FRC #{隊號} 的獎項(1/1)",
                                  url=f"https://www.thebluealliance.com/team/{隊號}/history",
                                  color=default_color)
            for i in m_team_awards:
                text = f"[{i['event_key']}](https://www.thebluealliance.com/event/{i['event_key']})"
                for n in i["recipient_list"]:
                    if n["team_key"] == f"frc{隊號}" and n["awardee"] is not None:
                        text += f" ({n['awardee']})"
                embed.add_field(name=i["name"], value=text)
            embeds_list = [embed]
        elif m_team_awards and len(m_team_awards) > 25:
            embeds_list = []
            pages_count = ceil(len(m_team_awards) / 25)
            for j in range(pages_count):
                temp_team_awards = m_team_awards[:25]
                embed = discord.Embed(title=f"FRC #{隊號} 的獎項({j + 1}/{pages_count})",
                                      url=f"https://www.thebluealliance.com/team/{隊號}/history",
                                      color=default_color)
                for i in temp_team_awards:
                    text = f"[{i['event_key']}](https://www.thebluealliance.com/event/{i['event_key']})"
                    for n in i["recipient_list"]:
                        if n["team_key"] == f"frc{隊號}" and n["awardee"] is not None:
                            text += f" ({n['awardee']})"
                    embed.add_field(name=i["name"], value=text)
                    m_team_awards.remove(i)
                embeds_list.append(embed)
        else:
            embed = discord.Embed(title=f"FRC #{隊號} 的獎項",
                                  url=f"https://www.thebluealliance.com/team/{隊號}/history",
                                  color=default_color)
            embed.add_field(name="沒有找到任何獎項資料。", value="該隊伍似乎尚未獲得任何獎項。", inline=False)
            embeds_list = [embed]
        for e in embeds_list:
            e.set_thumbnail(url=await self.get_avatar(隊號))
            e.set_footer(text="如要查看更多資訊，請點選標題連結進入TBA。")
            await ctx.channel.send(embed=e)


def setup(bot):
    bot.add_cog(TeamCmd(bot, bot.logger))
    bot.logger.info("\"TeamCmd\"已被載入。")
