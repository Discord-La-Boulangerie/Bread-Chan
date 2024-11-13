from typing import Optional
import discord
from discord.ext import commands
import datetime as dat
from discord import Member, Permissions, app_commands

class RoleGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="userroles", description="gestion des utilisateurs", guild_only=True, default_permissions=Permissions(moderate_members=True))


class RoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.role_group = RoleGroup()
        self.client.tree.add_command(self.role_group)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleCog(bot))
