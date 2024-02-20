import discord
from discord.ext import tasks
from discord import ChannelType
import json
import mysql.connector
from datetime import datetime
import pytz
import asyncio
import re

from final.BC.ClassModule import EpicBaseClass

# Utiliser le fuseau horaire pour la France (Europe/Paris)
timezone_fr = pytz.timezone('Europe/Paris')
# Obtenez la date et l'heure actuelles en France
now_in_fr = datetime.now(timezone_fr)

@tasks.loop(minutes=5)
async def ReloadPresence(client: discord.Client):
    """Change the bot's presence every 5 minutes"""
    state = discord.Activity(type=discord.ActivityType.watching,name=f"{len(client.guilds)} serveurs")
    await client.change_presence(activity=state)

@tasks.loop(minutes=15)
async def EpicNotifier(client: discord.Client):
    epicCli = EpicBaseClass()
    # Chargement des informations de la base de données depuis le fichier JSON
    with open('credentials.json', 'r') as fichier:
        donnees_json: dict = json.load(fichier)

    # Connexion à la base de données
    connexion = mysql.connector.connect(**donnees_json)
    curseur = connexion.cursor()
    pastEpic = ''  # Initialisez pastEpic à une valeur par défaut
    for guild in client.guilds:
        select_request = f"SELECT epic_games FROM game_notifier WHERE guild_id = {guild.id}"
        curseur.execute(select_request)
        result = curseur.fetchone()
        if result and result is dict:
            if bool(result[0]) == True:
                select_request = f"SELECT channel_id, webhook_id, role_ping_id FROM game_notifier WHERE guild_id = {guild.id}"
                curseur.execute(select_request)
                result_2 = curseur.fetchone()
                if result_2 and result_2 is dict:
                    if result_2[0] and result_2[1] and result_2[2]:
                        channel = client.get_channel(result_2[0])
                        webhook_id: int = result_2[1]
                        if channel and type(channel) is ChannelType.text:
                            webhook = discord.utils.get(await channel.webhooks(), id=webhook_id)
                            if webhook:
                                first_game = epicCli.games[0]
                                title = first_game.name

                                if pastEpic != title.casefold():
                                    emb = discord.Embed(title=title)
                                    emb.set_image(
                                        url=first_game.keyImages[0].url)
                                    await webhook.send(f"{f'<@&{result_2[2]}>' if result_2[2] is not None else ''} Nouveau jeu gratuit d'Epic Games !", embed=emb)

    # Fermer la connexion et le curseur
    curseur.close()
    connexion.close()