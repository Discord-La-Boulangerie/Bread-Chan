import mysql.connector
import json

# DB credentials
# Connexion à la base de données
with open('credentials.json', 'r') as fichier:
    donnees_json = json.load(fichier)
# Connexion à la base de données
connexion = mysql.connector.connect(**donnees_json)


select_request = f"SELECT welcome_channel_id, welcome_message, enabled, img_url FROM guild_welc where guild_id = 1190383960593809479"
curseur = connexion.cursor()
curseur.execute(select_request)
result = curseur.fetchall()
if result is not None:
    print(result[0][3])
    img, buffer = str(result[0][3]).split('?ex=') if result[0][3] is not None else ''

    print(img, buffer)