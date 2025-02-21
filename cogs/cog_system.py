import datetime as dat
import sys
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

SUPPORT_GUILD_ID = 1181845184288411688
support_guild = discord.Object(id=SUPPORT_GUILD_ID, type=discord.Guild)


class SystemCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    
    @app_commands.guilds(support_guild)
    @app_commands.command(name="sync", description="syncronise les commandes")
    async def sync(self, interaction: discord.Interaction):
        output = "commandes syncronisées avec succès !"
        try:
            await self.client.tree.sync()
            await self.client.tree.sync(guild=support_guild)
        except Exception as e:
            output = e
        await interaction.response.send_message(output, ephemeral=True)


    @app_commands.command(name="ping", description="pong ! 🏓")
    async def ping_pong(self, interaction: discord.Interaction):
        emb = discord.Embed(description=f"Pong ! 🏓 {round(self.client.latency, 1)} ms",
                            color=discord.Color.blurple(), timestamp=dat.datetime.now())
        await interaction.response.send_message(embed=emb, ephemeral=True)


    @app_commands.command(name="bot_info", description="permet d'obtenir les infos du bot")
    async def info(self, interaction: discord.Interaction):
        if interaction.client.user:
            emb = discord.Embed()
            emb.author.name = interaction.client.user.display_name
            emb.author.icon_url = interaction.client.user.display_avatar.url
            emb.set_footer(text=interaction.client.user,
                           icon_url=interaction.client.user.avatar)
            emb.add_field(
                name="Imports", value=f"Discord.py : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}\nBlaguesAPI : ?\nPython : {sys.version}", inline=False)
            await interaction.response.send_message(embed=emb, ephemeral=True)


    async def help_autocomplete(self, interaction: discord.Interaction, current: str):
        command_list = [command.name for command in self.client.walk_commands(
        ) if command.name != 'help' and current.lower() in command.name]
        command_name_list = [
            app_commands.Choice(name=commandName, value=commandName)
            for commandName in command_list if len(command_list) < 25
        ]
        return command_name_list


    @app_commands.command(name="help", description="commande d'aide")
    @app_commands.autocomplete(command_help=help_autocomplete)
    async def help_command(self, interaction: discord.Interaction, command_help: Optional[str], ephemeral: bool = True):
        msg = ""
        if not command_help:
            msg = "serveur de support : https://discord.gg/d6N8urV5pt \ncréer un ticket sur Github : https://github.com/Wishrito/Bread-Chan/issues/new"
        elif self.client.get_command(command_help) is not None:
            commande = self.client.get_command(command_help)
            if isinstance(commande, app_commands.Group):
                commands_groups = commande.walk_commands()
                msg = "cette commande est un groupe de commandes, en voici les commandes détaillées :\n"
                for group in commands_groups:
                    commande_details = commande.get_command(group.name)
                    if isinstance(commande_details, app_commands.Command):
                        msg += f"{commande_details.qualified_name} : {commande_details.description}\n\n"
            if isinstance(commande, app_commands.Command):
                msg = f"commande ``{commande.name}`` : {commande.description}"
        else:
            msg = f"commande ``{command_help}`` introuvable. veuillez réessayer."
        await interaction.response.send_message(msg, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    await bot.add_cog(SystemCog(bot))
