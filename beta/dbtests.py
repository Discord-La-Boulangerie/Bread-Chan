from typing import Optional
import discord
from discord import app_commands
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("discord_token")

# Configuration de la base de données SQLite
conn = sqlite3.connect('database.db')

cursor = conn.cursor()

# Créez la table si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        user_id INTEGER,
        role_id INTEGER,
        guild_id INTEGER,
        PRIMARY KEY (user_id, guild_id)
    )
''')
conn.commit()

# Configuration du bot Discord
intents = discord.Intents.all()

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        await self.tree.sync()
        await self.tree.sync(guild=guild_id1)
client = MyClient(intents=intents)
guild_id = 1130798906586959946
guild_id1 = discord.Object(id=guild_id)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user.name}')

# Commande pour obtenir un rôle
@client.tree.command(name="role-get")
async def get_role(interaction: discord.Interaction):
    # Vérifiez si l'utilisateur a déjà un rôle
    cursor.execute(f"SELECT role_id FROM roles WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
    result = cursor.fetchone()

    if result:
        await interaction.response.send_message("Vous avez déjà un rôle.")
    else:
        # Créer un nouveau rôle et l'ajouter à l'utilisateur
        role = await interaction.guild.create_role(name=f"{interaction.user.name}'s Role")
        await role.edit(position=interaction.user.top_role.position)
        await interaction.user.add_roles(role)

        # Stocker l'identifiant du rôle dans la base de données
        cursor.execute(f"INSERT INTO roles (user_id, role_id, guild_id) VALUES ({interaction.user.id}, {role.id}, {interaction.guild.id})")
        conn.commit()

        await interaction.response.send_message("Vous avez obtenu un nouveau rôle.")

# Commande pour configurer le nom et la couleur du rôle
@client.tree.command(name="role-setup")
@app_commands.describe(color="choisis une couleur dans la liste ou une couleur custom en HEX, RGB, HSL")
@app_commands.describe(name="change le nom de ton rôle")
async def setup_role(interaction: discord.Interaction, name: Optional[str] = None, color: Optional[str] = None):
    # Vérifiez si l'utilisateur a déjà un rôle
    cursor.execute(f"SELECT role_id FROM roles WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
    result = cursor.fetchone()
    if result:
        # Obtenez le rôle de l'utilisateur et mettez à jour le nom et la couleur
        role = interaction.guild.get_role(result[0])
        if name is None and color is None:
            await interaction.response.send_message("spécifie au moins un paramètre, s'il te plait.", ephemeral=True)

        if name and color:
            await role.edit(name=str(name), color=discord.Color.from_str(str(color)))
            await interaction.response.send_message(f"Le rôle {role.mention} a été mis à jour.", ephemeral=True)

        if name:
            await role.edit(name=str(name))
            await interaction.response.send_message(f"Le rôle {role.mention} a été mis à jour.", ephemeral=True)

        if color:
            await role.edit(color=discord.Color(int(color)))
            await interaction.response.send_message(f"Le {role.mention} a été mis à jour.", ephemeral=True)

    else:
        await interaction.response.send_message("Vous n'avez pas encore de rôle. Utilisez /role-get pour en obtenir un.", ephemeral=True)
    
# Exécutez le bot
client.run(str(token))