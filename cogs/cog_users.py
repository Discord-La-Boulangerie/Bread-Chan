import datetime as dat
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class UsersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot




async def setup(bot: commands.Bot):
    await bot.add_cog(UsersCog(bot))
