import os
from pathlib import Path
import discord
from discord import app_commands
from discord.ui import View, Modal
import sqlite3
from dotenv import load_dotenv

guild_id = 1163111703689576541
guild = discord.Object(guild_id)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        await self.tree.sync(guild=guild)

client = MyClient(intents=discord.Intents.all())

load_dotenv()
DISCORD_TOKEN = os.getenv("discord-token")

DbPath = Path("./database.sqlite")

connexion = sqlite3.connect(DbPath)
cursor = connexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS role_custom (
        user_id INTEGER,
        role_id INTEGER,
        guild_id INTEGER
    );
''')

connexion.commit()

class createModal(discord.ui.Modal):
    def __init__(self, e):
        self.e = e
        super().__init__(title="Candidature")
        
    role = discord.ui.TextInput(label='nom', style=discord.TextStyle.paragraph, max_length=50, placeholder="donne le nom de la commande :", required=True)
    code = discord.ui.TextInput(label='code', style=discord.TextStyle.paragraph, max_length=3000, placeholder="hésitez pas avec les détails, vous avez de la place", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        nom_fichier = f"{self.role.value}.py"
        nouvelle_ligne = f"import {self.role.value}"
        
        with open(nom_fichier, 'r') as fichier:
            contenu_existant = fichier.read()
        
        with open(nom_fichier, 'w') as fichier:
            fichier.write(nouvelle_ligne + '\n' + contenu_existant)

@client.event
async def on_ready():
    print("je suis en ligne !")
    SIO = client.get_guild(guild_id)
    for i in SIO.members:
        cursor.execute('''
            INSERT INTO guild_members (user_name, user_id, user_display_name, top_role_id)
            VALUES (?, ?, ?, ?)
        ''', (i.name, i.id, i.display_name, i.top_role.id))
    connexion.commit()

client.run(str(DISCORD_TOKEN))