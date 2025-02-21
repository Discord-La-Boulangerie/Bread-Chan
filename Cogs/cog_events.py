import datetime as dat
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if self.client.user:
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text:
                    emb = discord.Embed(
                        title="Merci", description=f"Salut, moi c'est {self.client.user.display_name} ! merci de m'avoir ajoutée au serveur ! je ferai de mon mieux pour répondre à tes attentes.\nsi jamais tu rencontre des problèmes, n'hésite pas à [Ouvrir un ticket](https://github.com/Wishrito/Bread-Chan/issues/new) !")
                    emb.set_author(name=self.client.user.display_name,
                                   icon_url=self.client.user.display_avatar.url)
                    await channel.send(embed=emb)
                    msg = f"je me suis permis de modifier la couleur de mon rôle, {bread_chan_role.mention}, j'espère que vous m'en voudrez pas trop 😉"
                    try:
                        bread_chan_role = discord.utils.get(
                            guild.roles, name="Bread Chan")
                        if bread_chan_role:
                            await bread_chan_role.edit(color=discord.Colour.orange())
                    except discord.errors.HTTPException as discord_err:
                        msg = f"une erreur est survenue : {discord_err}"
                    else:
                        await channel.send(msg)
                        break

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"connecté en tant que {self.client.user.name} ({self.client.user.id})")


async def setup(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))
