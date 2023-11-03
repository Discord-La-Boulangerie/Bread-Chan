import asyncio
import os
from dotenv import load_dotenv

import requests

load_dotenv()

api_key = os.getenv("bs_api_token")
async def brawlerlist():
    # URL de l'endpoint
    endpoint_url = "https://api.brawlstars.com/v1/brawlers"
    # Paramètres de l'en-tête
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # Effectuer la requête GET à l'endpoint
    response = requests.get(endpoint_url, headers=headers)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Le contenu de la réponse est au format JSON
        json_data = response.json()
        # Compter les items dont l'ID commence par 16
        count_items_starting_with_16 = 0
        for item in json_data.get("items", []):
            if str(item.get("id")).startswith("16"):
                count_items_starting_with_16 += 1
        return count_items_starting_with_16
    else:
        e = "La requête a échoué. Code d'état :", response.status_code
        return e
