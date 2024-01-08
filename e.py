import asyncio
from os import mkdir
import requests
import re

async def requete():
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
            title1, first_url1 = await telecharger_image(title, first_url)
            return title1, first_url1

    else:
        title, first_url = ""
        return title, first_url

async def fileWrite(fp: str, response):
    with open(fp, 'wb') as fichier:
        fichier.write(response.content)

async def telecharger_image(title: str, image_url: str) -> tuple[str, str]:
    # Faire une requête GET à l'URL de l'image
    response = requests.get(image_url)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        cleaned_title = re.sub(r"[^a-zA-Z0-9]+", '_', title)
        fpBase = "img/EpicNotifier/"
        fp = f"{fpBase}{cleaned_title}.jpg"
        
        # Enregistrer le contenu de l'image dans un fichier local
        try:
            await fileWrite(fp, response)
        except FileNotFoundError:
            mkdir(fpBase)
            await fileWrite(fp, response)
        else:
            return cleaned_title, fp
    else:
        cleaned_title, fp = ""
        return cleaned_title, fp

asyncio.run(requete())
