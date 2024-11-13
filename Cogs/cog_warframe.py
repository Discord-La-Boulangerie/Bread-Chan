import discord
from discord.ext import commands
from discord import Permissions, app_commands
import datetime as dat
from ClassModule import LoginModal
import pywmapi as wm

class WarframeGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="warframe", description="commandes relatives au jeu Warframe")

    @discord.app_commands.command(name="login", description="connexion à Warframe.market")
    async def warframeLogin(self, interaction: discord.Interaction):
        await interaction.response.send_modal(LoginModal())

    async def item_autocomplete(self, interaction: discord.Interaction, current: str):
        item_list = wm.items.get_orders(current)
        return [app_commands.Choice(name=item, value=item) for item in item_list]
    

class WarframeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.warframe_group = WarframeGroup()
        self.client.tree.add_command(self.warframe_group)

async def setup(bot: commands.Bot):
    await bot.add_cog(WarframeCog(bot))