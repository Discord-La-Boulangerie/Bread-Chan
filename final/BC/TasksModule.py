from turtle import listen
import discord
from discord.ext import tasks
import json
import requests
import mysql.connector
from datetime import datetime
import pytz
import asyncio
import re

# Utiliser le fuseau horaire pour la France (Europe/Paris)
timezone_fr = pytz.timezone('Europe/Paris')
# Obtenez la date et l'heure actuelles en France
now_in_fr = datetime.now(timezone_fr)

@tasks.loop(minutes=5)
async def ReloadPresence(client: discord.Client):
    """Change the bot's presence every 5 minutes"""
    state = discord.Activity(type=discord.ActivityType.watching,name=f"{len(client.guilds)} serveurs")
    await client.change_presence(activity=state)

async def requete() -> tuple[str, str]:
    # URL de l'API
    url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

    # Faire une requête GET à l'URL
    response = requests.get(url)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        # Charger le contenu JSON
        json_data = response.json()
        
        for element in json_data["data"]["Catalog"]["searchStore"]["elements"]:  # Accéder à la liste 'elements'
            title = element["title"]
            description = element["description"]

            # Récupérer le deuxième URL de keyImages
            first_url = element["keyImages"][0]["url"]

            print(f"Title: {title}\nDescription: {description}\nSecond URL: {first_url}\n")

            # Appeler la fonction pour télécharger l'image pour chaque titre et URL
            title, first_url = await telecharger_image(title, first_url)
            return title, first_url
        else:
            title, first_url = ""
            return title, first_url
    else:
        title, first_url = ""
        return title, first_url

async def telecharger_image(title: str, image_url: str) -> tuple[str, str]:
    # Faire une requête GET à l'URL de l'image
    response = requests.get(image_url)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        cleaned_title = re.sub(r"[^a-zA-Z0-9]+", '_', title)
        fp = f"img/EpicNotifier/{cleaned_title}.jpg"
        
        # Enregistrer le contenu de l'image dans un fichier local
        with open(fp, 'wb') as fichier:
            fichier.write(response.content)
        
        return cleaned_title, fp
    else:
        cleaned_title, fp = ""
        return cleaned_title, fp

@tasks.loop(minutes=15)
async def EpicNotifier(client: discord.Client):

    # Chargement des informations de la base de données depuis le fichier JSON
    with open('credentials.json', 'r') as fichier:
        donnees_json = json.load(fichier)

    # Connexion à la base de données
    connexion = mysql.connector.connect(**donnees_json)
    curseur = connexion.cursor()
    pastEpic = ''  # Initialisez pastEpic à une valeur par défaut
    for guild in client.guilds:
        select_request = f"SELECT epic_games FROM game_notifier WHERE guild_id = {guild.id}"
        curseur.execute(select_request)
        result = curseur.fetchone()
        if result:
            if bool(result[0]) == True:
                select_request = f"SELECT channel_id, webhook_id, role_ping_id FROM game_notifier WHERE guild_id = {guild.id}"
                curseur.execute(select_request)
                result_2 = curseur.fetchone()
                if result_2:
                    if result_2[0] and result_2[1] and result_2[2]:
                        channel = client.get_channel(result_2[0])
                        webhook_id = result_2[1]
                        if channel:
                            webhook = discord.utils.get(await channel.webhooks(), id=webhook_id)
                            if webhook:
                                # Appel de la fonction requete()
                                currentEpic, fp = await requete()
                                
                                if pastEpic != currentEpic:
                                    emb = discord.Embed(title=str(currentEpic))
                                    emb.set_image(url=fp)
                                    await webhook.send(f"{f'<@&{result_2[2]}>' if result_2[2] is not None else None} Nouveau jeu gratuit d'Epic Games !", embed=emb, file=discord.File(fp))

    # Fermer la connexion et le curseur
    curseur.close()
    connexion.close()