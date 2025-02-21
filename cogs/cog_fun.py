import datetime as dat
from typing import Optional

import discord
from blagues_api import BlaguesAPI, BlagueType
from discord import app_commands
from discord.ext import commands

from utils.ClassModule import sensitiveClass


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot





    @app_commands.command(name="random-joke", description="envoie une blague au hasard parmi une sélection")
    @app_commands.allowed_contexts(True, True, True)
    @app_commands.allowed_installs(True, True)
    async def rand_joke(self, interaction: discord.Interaction):
        blagues = BlaguesAPI(str(sensitiveClass.get_blagues_token()))
        random_joke = await blagues.random()
        await interaction.response.send_message(f"{random_joke.joke}\n\n||{random_joke.answer}||")


    @app_commands.command(name="specific-joke", description="envoie une blague d'un type spécifique")
    @app_commands.allowed_contexts(True, True, True)
    @app_commands.allowed_installs(True, True)
    @app_commands.choices(blaguetype=[app_commands.Choice(name=f"blague {blague.lower()}", value=blague) for blague in dir(BlagueType) if "__" not in blague and blague.isupper()])
    async def joke(self, interaction: discord.Interaction, blaguetype: app_commands.Choice[str]):
        blagues = BlaguesAPI(str(sensitiveClass.get_blagues_token()))
        categorized_joke = await blagues.random_categorized(blaguetype.value.lower())
        await interaction.response.send_message(f"{categorized_joke.joke}\n\n||{categorized_joke.answer}||")


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
