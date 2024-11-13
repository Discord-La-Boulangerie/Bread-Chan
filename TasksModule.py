from typing import Any
import discord
from discord.ext import tasks
from discord import ChannelType, Color
import json
import mysql.connector as db
import datetime as dat
import pytz


# Utiliser le fuseau horaire pour la France (Europe/Paris)
timezone_fr = pytz.timezone('Europe/Paris')
# Obtenez la date et l'heure actuelles en France
now_in_fr = dat.datetime.now(timezone_fr)

@tasks.loop(minutes=5)
async def ReloadPresence(client: discord.Client):
    """Change the bot's presence every 5 minutes"""
    state = discord.Activity(type=discord.ActivityType.watching,name=f"{len(client.guilds)} serveurs")
    await client.change_presence(activity=state)
    await client.get_guild(1181845184288411688).get_role(1210582053884661790).edit(color=Color.random())
