import json
import mysql.connector
# DB credentials
# Connexion à la base de données
with open('credentials.json', 'r') as fichier:
    donnees_json = json.load(fichier)
# Connexion à la base de données
connexion = mysql.connector.connect(**donnees_json)
request = f"SELECT epic_games FROM game_notifier WHERE guild_id = 1190383960593809479"
curseur = connexion.cursor()
curseur.execute(request)
result = curseur.fetchone()
print(result)
if result is not None:
   if result[0] == None:
      print(result[0])