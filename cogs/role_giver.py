import discord
from discord.ext import commands
import os
from pathlib import Path

import logger

error_color = 0xF1411C
default_color = 0x5FE1EA
base_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = str(Path(__file__).parent.parent.absolute())


class RoleGiver(commands.Cog):
    def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
        self.bot = bot
        self.real_logger = real_logger

    class JobGiverUI(discord.ui.View):
        def __init__(self, bot: commands.Bot, real_logger: logger.CreateLogger):
            super().__init__(timeout=None)
            self.bot = bot
            self.real_logger = real_logger

        @discord.ui.button(label="工程技術組", style=discord.ButtonStyle.blurple, custom_id="engineering")
        async def engineering(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1184087604468121642)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「工程技術組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「工程技術組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「工程技術組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「工程技術組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="資訊軟體組", style=discord.ButtonStyle.blurple, custom_id="programming")
        async def programming(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1184089055231746118)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「資訊軟體組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「資訊軟體組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「資訊軟體組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「資訊軟體組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="活動規劃組", style=discord.ButtonStyle.blurple, custom_id="event_planning")
        async def event_planning(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1192497659139854436)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「活動規劃組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「活動規劃組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「活動規劃組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「活動規劃組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="交流公關組", style=discord.ButtonStyle.blurple, custom_id="public_relations")
        async def public_relations(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1184093105805344818)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「交流公關組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「交流公關組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「交流公關組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「交流公關組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="美宣設計組", style=discord.ButtonStyle.blurple, custom_id="art_design")
        async def art_design(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1184093718060470292)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「美宣設計組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「美宣設計組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「美宣設計組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「美宣設計組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="行政文書組", style=discord.ButtonStyle.blurple, custom_id="administration")
        async def administration(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1184094478638784573)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「行政文書組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「行政文書組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「行政文書組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「行政文書組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="教學製作組", style=discord.ButtonStyle.blurple, custom_id="education")
        async def education(self, button, interaction: discord.Interaction):
            server = self.bot.get_guild(1172902183205871747)
            role = server.get_role(1192497836781224017)
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                self.real_logger.info(f"給予 {interaction.user} 「教學製作組」身分組")
                embed = discord.Embed(title="成功！", description="已給予「教學製作組」身分組！", color=default_color)
                embed.set_footer(text="如要移除身分組，請再次點擊按鈕")
            else:
                await interaction.user.remove_roles(role)
                self.real_logger.info(f"移除 {interaction.user} 「教學製作組」身分組")
                embed = discord.Embed(title="成功！", description="已移除「教學製作組」身分組！", color=default_color)
                embed.set_footer(text="如要重新獲得身分組，請再次點擊按鈕")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.slash_command(name="role_giver", description="傳送「選取身分組」訊息", guild_ids=[1172902183205871747,
                                                                                    857996539262402570])
    @commands.has_role(1193209412018524180)
    async def role_giver(self, ctx):
        await ctx.respond("即將在此頻道建立職位選取器...", ephemeral=True)
        embed = discord.Embed(title="選取組別", description="請選擇你希望負責的工作，以獲得對應的權限。", color=default_color)
        embed.add_field(name="工程技術組", value="製作模擬賽模擬場地&場地布置、負責周邊小物打印製作", inline=False)
        embed.add_field(name="資訊軟體組", value="FMS系統復刻、Discord bot整合系統製作&維護、維護網站、維護PMS系統", inline=False)
        embed.add_field(name=" ", value="---------------", inline=False)
        embed.add_field(name="活動規劃組", value="對內活動企劃書編輯、模擬賽&季後賽活動規劃", inline=False)
        embed.add_field(name="交流公關組", value="對外活動企劃書編輯、 聯盟募款、聯盟社群帳號建立&宣傳", inline=False)
        embed.add_field(name=" ", value="---------------", inline=False)
        embed.add_field(name="美宣設計組", value="聯盟宣傳圖稿、周邊小物設計、活動攝影紀錄、影音剪輯", inline=False)
        embed.add_field(name="行政文書組", value="聯盟會議記錄、經費管理&紀錄、聯盟財產清冊紀錄(如後續有需求)", inline=False)
        embed.add_field(name=" ", value="---------------", inline=False)
        embed.add_field(name="教學製作組", value="製作機器人加工技術、程式撰寫技術、電控配電技術等類型之文檔", inline=False)
        embed.set_footer(text="「每人至多一次加入兩種組別，加入後請負責！」 - 山貓，2024")
        await ctx.send(embed=embed, view=self.JobGiverUI(self.bot, self.real_logger))

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(self.JobGiverUI(self.bot, self.real_logger))


def setup(bot):
    bot.add_cog(RoleGiver(bot, bot.logger))
    bot.logger.info("\"RoleGiver\"已被載入。")
