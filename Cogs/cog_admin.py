import asyncio
import json
import os
import sys
from typing import Any
import discord
from discord.ext import commands
from discord import ChannelType, Permissions, app_commands
import datetime as dat

support_guild_id = 1181845184288411688

class SudoGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="sudo", description="commandes admin", guild_ids=[support_guild_id], default_permissions=Permissions(administrator=True))

    @app_commands.command(name="get_all_emojis", description="renvoie tous les emojis que le bot voit")
    async def get_all_emojis(self, interaction: discord.Interaction):
        sysGuilds = [1091096575280947404, 1001496918343553094]
        emb = discord.Embed()
        emb.description = str([emoji.name for emoji in interaction.client.emojis if emoji.guild_id in sysGuilds])
        await interaction.response.send_message(embed=emb, ephemeral=True)


    @app_commands.command(name="get_badges", description="test")
    async def get_badges(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.channel and interaction.channel.type == ChannelType.text:
            await interaction.response.send_message(user.public_flags.all(), ephemeral=True)



async def leave_autocomplete(interaction: discord.Interaction, current: str):
    guildsList = [
        guild.name for guild in interaction.client.guilds
        if guild.id not in [916847454115229726, 1163111703689576541, 989629222404386847, 1001496918343553094] and current in guild.name.casefold()
    ]

    return [
        app_commands.Choice(name=guild, value=guild)
        for guild in guildsList
    ]

sudoGroup = SudoGroup()

class BreadChanGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="bread-chan", description="commandes admin pour Bread Chan", parent=sudoGroup)


    @app_commands.command(name="leave_guild", description="Quitte un serveur spécifié")
    @app_commands.autocomplete(serveur=leave_autocomplete)
    async def leave(self, interaction: discord.Interaction, serveur: str):
        gld = discord.utils.get(interaction.client.guilds, name=serveur)
        if gld:
            await gld.leave()
            emb = discord.Embed(
                title="Succès !", description=f"Je suis maintenant déconnecté de {gld.name}", color=0x2ecc71)
            await interaction.response.send_message(embed=emb, ephemeral=True)
    
    
    @app_commands.command(name="reboot", description="redémarre le bot")
    async def reboot(self, interaction: discord.Interaction):
        if interaction.client.application:
            if interaction.client.application.team:
                if interaction.user.id == interaction.client.application.owner.id:
                    current_script = sys.argv[0]
                    emb = discord.Embed()
                    TimeReboot = dat.datetime.now() + dat.timedelta(seconds=5)
                    TimeRebootTotimestamp = round(TimeReboot.timestamp())
                    emb.description = f"Je vais redémarrer <t:{TimeRebootTotimestamp}:R>"
                    await interaction.response.send_message(embed=emb, ephemeral=True, delete_after=TimeReboot.second)
                    await asyncio.sleep(TimeReboot.second)
                    os.execv(sys.executable, [
                             sys.executable, current_script] + sys.argv[1:])
                elif interaction.client.application.team.owner:
                    await interaction.response.send_message(f'seul mon possesseur, {interaction.client.application.team.owner.mention}, est habilité à me redémarrer', ephemeral=True)

class SudoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sudo_group = SudoGroup()
        self.bot.tree.add_command(self.sudo_group)

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bread_chan_group = BreadChanGroup()
        self.bot.tree.add_command(self.bread_chan_group)


async def setup(bot: commands.Bot):
    await bot.add_cog(SudoCog(bot))
    await bot.add_cog(AdminCog(bot))
