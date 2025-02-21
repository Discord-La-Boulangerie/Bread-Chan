from ast import literal_eval
import asyncio
import datetime as dat
import json
import os
from pathlib import Path
import random
import re
import sys
from typing import Any, Optional, cast

import discord
import mysql.connector as db
from blagues_api import BlaguesAPI, BlagueType
from discord import ChannelType, Spotify, app_commands
from discord.ext import commands
from discord.gateway import DiscordWebSocket, _log
from discord.permissions import *

import utils.ClassModule as ClassModule
import TasksModule
from utils.ClassModule import SensitveClass


# Fonction pour charger les cogs
async def load_cogs(bot: commands.Bot):
    print(Path(__file__).parent / "cogs")
    modules = [
        file.stem for file in (
            Path(__file__)
            .parent
            / "cogs"
        ).glob("cog_*.py")
    ]
    for module in modules:
        try:
            await bot.load_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            msg = f"Failed to load {module}: {e}"
        else:
            cog = bot.cogs.get(f"cogs.{module}")
            msg = f"Loaded {module}"
        print(msg)

# mobile status


async def identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': sys.platform,
                '$browser': 'Discord Android',
                '$device': 'Discord Android',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload['d']['shard'] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }

    if state._intents is not None:
        payload['d']['intents'] = state._intents.value

    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)
    _log.info('Shard ID %s has sent the IDENTIFY payload.', self.shard_id)

DiscordWebSocket.identify = identify

# Crée une instance de SensitveClass
sensitiveClass = SensitveClass()


SUPPORT_GUILD_ID = 1181845184288411688
support_guild = discord.Object(id=SUPPORT_GUILD_ID, type=discord.Guild)
intents = discord.Intents.all()

blagueGroup = app_commands.Group(name="blague", description="système de blagues")

searchGroup = app_commands.Group(
    name="search", description="groupe contenant les différentes commandes de recherche")

# command group for games
# gamegroup = app_commands.Group(name="game", description="group de commandes de jeux")
hsrGroup = app_commands.Group(name="hsr", description="commandes du jeu Honkai Star Rail")
# fortniteGroup = app_commands.Group(parent=gamegroup, name="fortnite")

# discord client def


class BreadChanClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.set_translator(ClassModule.BreadChan_Translator())
        await self.tree.sync(guild=support_guild)
        await self.tree.sync()


client = BreadChanClient(intents=intents)
emojiGuild = client.get_guild(1001496918343553094)


@client.tree.command(name="spotify-send-track", description="envoie la musique écoutée sur Spotify")
@app_commands.allowed_contexts(True, True, True)
@app_commands.allowed_installs(True, True)
async def spotify_track(interaction: discord.Interaction):
    msg = ""
    ephemeral = False
    member = interaction.user.mutual_guilds[0].get_member(interaction.user.id)
    if member:
        spotify_activity = discord.utils.find(
            lambda a: isinstance(a, discord.Spotify), member.activities)
        if isinstance(spotify_activity, Spotify):
            msg = spotify_activity.track_url
        else:
            msg = "Aucune musique en cours d'écoute 🥲"
            ephemeral = True
    else:
        msg = "nous n'avons pas de serveurs en commun, je ne peux donc pas accéder à ce que tu écoutes :("
        ephemeral = True
    await interaction.response.send_message(msg, ephemeral=ephemeral)


@app_commands.context_menu(name="Say")
@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
async def say(interaction: discord.Interaction, message: discord.Message):
    if interaction.channel and interaction.channel.type == ChannelType.text:
        await interaction.response.send_modal(ClassModule.SayModal(message))
        await interaction.channel.typing()

@app_commands.context_menu(name="Profil")
@app_commands.rename(user="Membre")
@app_commands.allowed_installs(True, True)
@app_commands.allowed_contexts(True, True, True)
async def profil(interaction: discord.Interaction, user: discord.Member):
    if client.user:
        badges_class = []
        if user.public_flags.all() is not None:
            badges_class.extend([
                f"{discord.utils.get(client.emojis, name=badge.name)}" for badge in user.public_flags.all()])
        else:
            badges_class = ["aucun badge"]
        badges = ' '.join(badges_class)
        if user.accent_color is not None:
            nitro_role = discord.utils.get(
                client.emojis, id=1222184055156637726)
            badges_class.append(f"{nitro_role}")
        # Tu peux meme foutre ca en bas, ca precise a quel heure a ete fait l'embed
        emb = discord.Embed(title=f"Profil de {user.display_name}",
                            url=f"https://discord.com/users/{user.id}", color=user.color, timestamp=dat.datetime.now())
        emb.add_field(name="Date de création du compte :",
                      value=f"le {discord.utils.format_dt(user.created_at)}")
        if interaction.context.guild:
            emb.add_field(name="Badges :", value=badges)
        # Pour ajouter la pp du type
        emb.set_thumbnail(url=f"{user.display_avatar}")
        # Perso je fous les infos du bot la dessus
        emb.set_footer(text=client.user,
                       icon_url=client.user.avatar)
        # type: ignore
        await interaction.response.send_message(embed=emb, ephemeral=True)



client.tree.add_command(searchGroup)


async def main():
    await load_cogs(client)
    await client.start(sensitiveClass.get_discord_token())

if __name__ == "__main__":
    asyncio.run(main())
