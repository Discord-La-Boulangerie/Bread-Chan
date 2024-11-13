import calendar
from typing import Optional, Union
import discord
from discord.ext import commands
import datetime as dat
from discord import Member, Permissions, app_commands
from discord.app_commands import locale_str as locale

class ModerationGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="moduser", description=locale("gestion des utilisateurs"),
                         guild_only=True, default_permissions=Permissions(moderate_members=True))

    @app_commands.command(name="mute", description="mute l'utilisateur sélectionné")
    @app_commands.rename(user="utilisateur", timeout="durée", reason="raison")
    @app_commands.describe(user="l'utilisateur à mute", timeout="le temps du mute", reason="la raison du mute")
    @app_commands.choices(timeout=[
        app_commands.Choice(name="5 minutes", value="5"),
        app_commands.Choice(name="10 minutes", value="10"),
        app_commands.Choice(name="15 minutes", value="15"),
        app_commands.Choice(name="30 minutes", value="30"),
        app_commands.Choice(
            name="1 heure", value=f"{dat.timedelta(hours=1).total_seconds()}"),
        app_commands.Choice(
            name="2 heures", value=f"{dat.timedelta(hours=2).total_seconds()}"),
        app_commands.Choice(
            name="6 heures", value=f"{dat.timedelta(hours=6).total_seconds()}"),
        app_commands.Choice(
            name="12 heures", value=f"{dat.timedelta(hours=12).total_seconds()}"),
        app_commands.Choice(
            name="1 jour", value=f"{dat.timedelta(days=1).total_seconds()}"),
        app_commands.Choice(
            name="1 semaine", value=f"{dat.timedelta(weeks=1).total_seconds()}"),
        app_commands.Choice(name="pour le reste du mois",
                            value=f"{(calendar.monthrange(dat.datetime.now(dat.UTC).year, dat.datetime.now(dat.UTC).month)[1] - dat.datetime.now(dat.UTC).day) * 24 * 60 * 60}")
    ])
    async def muteUser(self, interaction: discord.Interaction, user: discord.Member, timeout: Optional[app_commands.Choice[str]] = None, reason: Optional[str] = None):
        msg: str = ""
        if timeout is None:
            timeout = app_commands.Choice(name="10 minutes", value="10")

        elif isinstance(interaction.user, Member) and interaction.user == user:
            msg = f"{user.mention} pourquoi t'as essayé de te mute ???"
        else:
            print(timeout.value, timeout.name)
            await user.timeout(dat.timedelta(seconds=int(timeout.value)), reason=f"{interaction.user.name} | {reason}" if reason is not None else f"{interaction.user.name} | manquement aux règles")
            msg = f"{user.mention} a bien été mute {timeout.name}."

        await interaction.response.send_message(msg, ephemeral=True)


    @app_commands.command(name="ban", description="bannit l'utilisateur sélectionné")
    @app_commands.rename(user="utilisateur", reason="raison", delete_msgs="supression-messages")
    @app_commands.describe(user="l'utilisateur à ban", reason="la raison du ban", delete_msgs="les messages à effacer en jours")
    @app_commands.choices(delete_msgs=[app_commands.Choice(name=str(i), value=i) for i in range(1,8)])
    async def banUser(self, interaction: discord.Interaction, user: discord.Member, reason: Optional[str], delete_msgs: app_commands.Choice[int]):
        msg: str
        if interaction.user == user:
            msg = f"{user.mention} pourquoi t'as essayé de te ban ???"
        else:
            await user.ban(reason=f"{interaction.user.name} | {reason}" if reason is not None else f"{interaction.user.name} | manquement aux règles", delete_message_days=delete_msgs.value)
            msg = f"{user.mention} a bien été banni."
        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(name="nuke", description="nuke le chat sélectionné")
    async def nuke(self, interaction: discord.Interaction, channel: Optional[Union[discord.TextChannel, discord.VoiceChannel]] = None):
        msg = ""
        if channel is None:
            channel = interaction.channel
        if channel is not None:
            try:
                nukedChannelPosition = channel.position
                clonedChannel = await channel.clone()
                await channel.delete()
                await clonedChannel.edit(position=nukedChannelPosition)
            except Exception as e:
                msg = e
            else:
                msg = f"le channel {channel.name} a bien été nuke."
            finally:
                if channel == interaction.channel:
                    await clonedChannel.send(content=str(msg), delete_after=5)
                elif channel != interaction.channel:
                    await interaction.response.send_message(content=str(msg), delete_after=5)

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.moderation_group = ModerationGroup()
        self.client.tree.add_command(self.moderation_group)




async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
