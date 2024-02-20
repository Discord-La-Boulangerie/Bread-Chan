import re
import ClassModule
from ClassModule import RiskVar

import TasksModule

from typing import Optional, cast
import mysql.connector
import random
import json
import asyncio
import sys
import os
import datetime

# import des API
import enkanetwork as enk
import discord
from discord import ChannelType, app_commands
from discord.ext import tasks
from discord.gateway import DiscordWebSocket, _log

#mobile status
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

# Crée une instance de RiskVar
risk_var_instance = RiskVar()
guild_id = 1181845184288411688
guild_id1 = discord.Object(id=guild_id)
intents = discord.Intents.all()

enkaclient = enk.EnkaNetworkAPI(lang="fr", cache=True)


# discord client def
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
        await self.tree.sync(guild=guild_id1)
        await self.tree.sync()

client = MyClient(intents=intents)

@client.tree.command(name="ping", description="[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb=discord.Embed(description=f"Pong ! 🏓 {round(client.latency, 1)} ms", color=discord.Color.blurple(),timestamp=datetime.datetime.now())
    await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="bot_info", description="permet d'obtenir les infos du bot")
async def botinfo(interaction: discord.Interaction):
    if client.user:
        emb = discord.Embed()
        emb.author.name = client.user.display_name
        emb.author.icon_url = client.user.display_avatar.url
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        emb.add_field(name="Imports", value=f"Discord.py : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}\nEnkanetwork.py :{enk.__version__}\nBlaguesAPI : ?\nPython : {sys.version}", inline=False)
        await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="help", description="commande d'aide")
async def helpCommand(interaction: discord.Interaction, ephemère: Optional[bool] = True):
    await interaction.response.send_message("serveur de support : https://discord.gg/fSZdtyrEz8 \ncréer un ticket sur Github : https://github.com/Wishrito/Bread-Chan/issues/new ", ephemeral=bool(ephemère))

@client.tree.command(name="genshin_profil", description="obtenir des infos sur un compte Genshin Impact")
@app_commands.describe(uid="le pseudo ou identifiant de l'utilisateur")
async def genshininfo(interaction: discord.Interaction, uid: str):
        if client.user:
            try: 
                data = await enkaclient.fetch_user(uid)
            except enk.EnkaPlayerNotFound as vr:
                emb=discord.Embed(title="Erreur", url="https://enka.network/404", description=f"=== UID introuvable ===\n\n{vr}", color = discord.Colour.red(), timestamp=datetime.datetime.now())
                emb.set_thumbnail(url=f"{interaction.user.display_icon}") #type: ignore
                emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
                await interaction.response.send_message(embed=emb, ephemeral=True)
            else:
                emb=discord.Embed(title=f":link: Vitrine Enka de {data.player.nickname}", url=f"https://enka.network/u/{uid}", description=f"=== Infos du compte ===\n\nRang d'aventure: {data.player.level} | Niveau du monde: {data.player.world_level}\n\nBio: {data.player.signature}\n\n<:achievements:1129447087667433483> Succès: {data.player.achievement}\n\n<:abyss:1129447202566180905> Profondeurs spiralées : étage {data.player.abyss_floor} | salle {data.player.abyss_room}", color = discord.Color.blue(), timestamp=datetime.datetime.now())
                emb.set_author(name=f"{client.user}", url=f"https://discordapp.com/users/{client.user.id}", icon_url=client.user.avatar)
                emb.set_thumbnail(url=f"{data.player.avatar.icon.url}")
                emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
                await interaction.response.send_message(embed=emb, ephemeral=True, view=ClassModule.DropdownView(data))

@client.tree.command(name="role_create", description="Permet de créer un rôle custom")
@app_commands.guild_only()
async def createrole(interaction: discord.Interaction):
    if client.user and interaction.guild:
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        select_request = f"SELECT role_id FROM user_roles WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
        curseur = connexion.cursor()
        curseur.execute(select_request)
        result = curseur.fetchone()
        owner = client.get_user(client.application.team.owner.id)
        await owner.send(result)
        if result: # Si il n'y a pas de résultat (aucun rôle trouvé)
            await interaction.response.send_message(f"Vous avez déjà obtenu un rôle sur ce serveur : <@&{result[0]}>", ephemeral=True)

        else:
            role = await interaction.guild.create_role(name=f"rôle custom de {interaction.user.name}")
            await interaction.user.add_roles(role)
            insert_request = f"INSERT INTO user_roles (role_id, user_id, guild_id) VALUES ({role.id}, {interaction.user.id}, {interaction.guild.id})"
            curseur.execute(insert_request)
            selfUser = interaction.guild.get_member(client.user.id)
            if interaction.user.top_role.position > selfUser.top_role.position:
                await interaction.response.send_message(f"vous avez obtenu un rôle, cependant du à un manque de permissions, il est nécessaire que le rôle soit déplacé manuellement.")
            else:
                if interaction.user:
                    await role.edit(position=interaction.user.top_role.position)
                    await interaction.response.send_message(f"Vous avez obtenu un rôle sur ce serveur.", ephemeral=True)

        # Fermeture du curseur et de la connexion
        connexion.commit()
        connexion.close()

@client.tree.command(name="role_edit", description="Permet de modifier votre rôle")
@app_commands.guild_only()
async def editrole(interaction: discord.Interaction, name: Optional[str] = None, color: Optional[str] = None):
    # DB credentials
    # Connexion à la base de données
    with open('credentials.json', 'r') as fichier:
        donnees_json = json.load(fichier)

    # Connexion à la base de données
    connexion = mysql.connector.connect(**donnees_json)

    select_request = f"SELECT role_id FROM user_roles WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}"
    curseur = connexion.cursor()
    curseur.execute(select_request)
    result = curseur.fetchone()

    if not result:  # Si il n'y a pas de résultat (aucun rôle trouvé)
        await interaction.response.send_message("Vous n'avez pas encore de rôle personnalisé.", ephemeral=True)
    else:
        if interaction.guild:
            role = interaction.guild.get_role(int(result[0]))
            if name is None and color is None:
                await interaction.response.send_message("Vous devez spécifier au moins un argument", ephemeral=True)
            else:
                try:
                    if name is not None:
                        if role:
                            await role.edit(name=name)

                    if color is not None:
                        if role:
                            await role.edit(color=discord.Color.from_str(color))
                except ValueError as VE:
                    await interaction.response.send_message(f"Une erreur est survenue : {VE}", ephemeral=True)

                else:
                    await interaction.response.send_message("votre rôle a été mis à jour.", ephemeral=True)

    # Fermeture du curseur et de la connexion
    connexion.commit()
    connexion.close()

async def guild_autocomplete(interaction: discord.Interaction, current: str):
    response = [guild.name for guild in client.guilds if guild.id != 916847454115229726 and guild.id != 1163111703689576541 and guild.id != 1001496918343553094]
    return [
        app_commands.Choice(name=guild_name, value=guild_name)
        for guild_name in response
    ]

@client.tree.command(name="reboot", description="redémarre le bot", guild=guild_id1)
@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
async def reboot(interaction: discord.Interaction):
    if client.application:
        if client.application.team:
            if interaction.user == client.application.team.owner:
                current_script = sys.argv[0]
                emb = discord.Embed()
                TimeReboot = datetime.datetime.now() + datetime.timedelta(seconds=5)
                TimeRebootTotimestamp = round(TimeReboot.timestamp())
                emb.description = f"Je vais redémarrer <t:{TimeRebootTotimestamp}:R>"
                await interaction.response.send_message(embed=emb, ephemeral=True)
                await asyncio.sleep(5)
                os.execv(sys.executable, [sys.executable, current_script] + sys.argv[1:])
            else:
                if client.application.team.owner:
                    await interaction.response.send_message(f'seul mon possesseur, {client.application.team.owner.global_name}, est habilité à me redémarrer', ephemeral=True)

@client.tree.command(name="get_partner_invite", description="permet d'obtenir l'accès à un serveur partenaire")
@app_commands.default_permissions(administrator=True)
@app_commands.autocomplete(serveur=guild_autocomplete)
async def inviteServ(interaction: discord.Interaction, serveur: str):
    gld = discord.utils.get(client.guilds, name=serveur)

    if gld is None:
        await interaction.response.send_message("Le serveur spécifié n'a pas été trouvé.", ephemeral=True)
        return

    try:
        invited = await gld.text_channels[0].create_invite(max_uses=1)
        await interaction.response.send_message(f"Voici le lien d'invitation pour {serveur}: {invited}", ephemeral=True)
    except discord.errors.Forbidden:
        await interaction.response.send_message("Je n'ai pas la permission de créer des invitations dans ce serveur.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Une erreur s'est produite : {e}", ephemeral=True)

@client.tree.command(name="leave_guild", description="Quitte un serveur spécifié")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.autocomplete(serveur=guild_autocomplete)
async def leave(interaction: discord.Interaction, serveur: str):
    gld = discord.utils.get(client.guilds, name=serveur)
    if gld:
        await gld.leave()
        emb = discord.Embed(title="Succès !",description=f"Je suis maintenant déconnecté de {gld.name}",color=0x2ecc71)
        await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="config_welcome", description="Configuration du système de bienvenue")
@app_commands.default_permissions(manage_guild=True)
@app_commands.guild_only()
@app_commands.choices(option=[
    app_commands.Choice(name="Salon de bienvenue", value="welcome_ID"),
    app_commands.Choice(name="Message de bienvenue", value="welcome_MSG"),
    app_commands.Choice(name="Définir les deux", value="welcome_ID_&_MSG")
])
async def configWelc(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]] = None, enabled: Optional[bool] = True, image_url: Optional[str] = None):
    if client.user and interaction.guild:
        owner = client.get_user(client.application.team.owner.id)
        
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        emb = discord.Embed(title="config_welcome : configuration actuelle")
        emb.set_author(name=client.user.display_name, url=f"https://discord.com/users/{client.user.id}", icon_url=client.user.display_avatar.url)

        if option == None and enabled == True and image_url == None:
            select_request = f"SELECT welcome_channel_id, welcome_message, enabled, img_url FROM guild_welc where guild_id = {interaction.guild.id}"
            curseur = connexion.cursor()
            curseur.execute(select_request)
            result = curseur.fetchone()
            if result:
                await owner.send(f'result1 = {result}')
                img = result[3]
                activated = str(bool(result[2])).replace('True', 'Oui').replace('False', 'Non')
                img_txt = " Aucune image de bienvenue n\'a été définie" if str(img) == 'None' else ''
                channel = interaction.guild.get_channel(result[0])
                emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
                print(img)
                if str(img) != "None":
                    emb.set_image(url=img)
                await interaction.response.send_message(embed=emb, ephemeral=True)
            else:
                await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
            curseur.close()
        else:
            style = discord.TextStyle.paragraph
            lenght = 0
            if image_url != None:
                if "?ex=" in image_url:
                    image_url, buffer = image_url.split("?ex=")

            if option != None and option.value != 'welcome_ID_&_MSG':
                if option.value == "welcome_ID":
                    lenght = 20
                    style = discord.TextStyle.short
                elif option.value == "welcome_MSG":
                    lenght = 4000
                    style = discord.TextStyle.long
                await interaction.response.send_modal(ClassModule.WelcomeModal(option.value, lenght, style, enabled, image_url))
            else:
                await interaction.response.send_modal(ClassModule.WelcomeModal(option.value if option is not None else "Modal", lenght, style, enabled, image_url))
            await owner.send(f"{option} {enabled} {image_url}")
        connexion.close()


@client.tree.command(name="config_goodbye", description="Configuration du système de départs")
@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
@app_commands.choices(option=[
    app_commands.Choice(name="Salon de départ", value="bye_ID"),
    app_commands.Choice(name="Message de départ", value="bye_MSG"),
    app_commands.Choice(name="Définir les deux", value="bye_ID_&_MSG")
])
async def configBye(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]] = None, enabled: Optional[bool] = True, image_url: Optional[str] = None):
    if client.user and interaction.guild:
        owner = client.get_user(client.application.team.owner.id)
        
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        emb = discord.Embed(title="config_goodbye : configuration actuelle")
        emb.set_author(name=client.user.display_name, url=f"https://discord.com/users/{client.user.id}", icon_url=client.user.display_avatar.url)

        if option == None and enabled == True and image_url == None:
            select_request = f"SELECT goodbye_channel_id, goodbye_message, enabled, img_url FROM guild_bye where guild_id = {interaction.guild.id}"
            curseur = connexion.cursor()
            curseur.execute(select_request)
            result = curseur.fetchone()
            if result:
                await owner.send(f'result1 = {result}')
                img = result[3]
                activated = str(bool(result[2])).replace('True', 'Oui').replace('False', 'Non')
                img_txt = " Aucune image de départ n\'a été définie" if str(img) == 'None' else ''
                channel = interaction.guild.get_channel(result[0])
                emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
                print(img)
                if str(img) != "None":
                    emb.set_image(url=img)
                await interaction.response.send_message(embed=emb, ephemeral=True)
            else:
                await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
            curseur.close()
        else:
            style = discord.TextStyle.paragraph
            lenght = 0
            if image_url != None:
                if "?ex=" in image_url:
                    image_url, buffer = image_url.split("?ex=")

            if option != None and option.value != 'bye_ID_&_MSG':
                if option.value == "bye_ID":
                    lenght = 20
                    style = discord.TextStyle.short
                elif option.value == "bye_MSG":
                    lenght = 4000
                    style = discord.TextStyle.long
                await interaction.response.send_modal(ClassModule.ByeModal(option.value, lenght, style, enabled, image_url))
            else:
                await interaction.response.send_modal(ClassModule.ByeModal(option.value if option is not None else "Modal", lenght, style, enabled, image_url))
            await owner.send(f"{option} {enabled} {image_url}")
        connexion.close()


@client.tree.command(name="config_epic_notifier", description="configuration du système d'annonces de jeux gratuits")
@app_commands.guild_only()
async def gameNotifier(interaction: discord.Interaction, option: Optional[bool] = True, channel: Optional[discord.TextChannel] = None, mention: Optional[discord.Role] = None):
    if option != None and mention != None:
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        request = f"SELECT epic_games, webhook_id, channel_id, role_ping_id FROM game_notifier WHERE guild_id = {interaction.guild.id}"
        curseur = connexion.cursor()
        curseur.execute(request)
        result = curseur.fetchone()
        print(result)
        if result is not None and interaction.guild:
            base_request = "INSERT INTO auto_roles (guild_id"
            values = [interaction.guild.id]

            if result[0] is None:
                base_request += ", epic_games"
                values.append(option)

            if result[1] is None:
                guild = client.get_guild(interaction.guild.id)
                channel_id = guild.get_channel(result[2])
                avatar = client.user.avatar.read()
                webhook = await channel_id.create_webhook(name=f"{client.user.display_name}'s Epic Deals", avatar=avatar)
                base_request += ", webhook_id"
                values.append(webhook.id)

            if result[2] is None:
                base_request += ', channel_id'
                values.append(channel.id)

            if result[3] is None:
                base_request += ", role_ping_id"
                values.append(mention.id)

            base_request += ") VALUES (" + ", ".join(map(str, values)) + ") WHERE guild_id = {interaction.guild.id}"
            request = base_request

                # INSERT INTO auto_roles (guild_id, epic_games, webhook_id, channel_id, role_ping_id) VALUES ({interaction.guild.id}, {option}, {webhook.id}, {channel_id}, {role.id}) WHERE guild_id = {interaction.guild.id}
            print(request)

        else:
            base_request = "UPDATE game_notifier SET guild_id"
            values = [interaction.guild.id]

            base_request_2 = ""
            base_request_3 = ""
            base_request_4 = ""

            request_end = f" WHERE guild_id = {interaction.guild.id}"

            if option is not None:
                base_request += ", epic_games"
                values.append(option)
            else:
                base_request += ", epic_games = NULL"

            if channel is not None:
                base_request += ', channel_id'
                values.append(channel.id)
            else:
                base_request += ', channel_id = NULL'

            if mention is not None:
                base_request += ", role_ping_id"
                values.append(mention.id)
            else:
                base_request += ", role_ping_id = NULL"

            request = base_request + ") VALUES (" + ", ".join(map(str, values)) + request_end

            
            # UPDATE game_notifier SET guild_id = {interaction.guild.id}, epic_games = {option}, channel_id = {channel.id}, role_ping_id = {mention.id} WHERE guild_id = {interaction.guild.id}
            print(request)


        curseur.execute(request)

        await interaction.response.send_message("le système EpicGamesNotifier pour ce serveur a été configuré avec succès", ephemeral=True)

        # Fermeture de la connexion et commit
        connexion.commit()
        connexion.close()


@client.tree.command(name="config_auto_role", description="configuration des rôles automatiques")
@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
async def auto_role_setup(interaction: discord.Interaction, role_1: Optional[discord.Role] = None, role_2: Optional[discord.Role] = None, role_3: Optional[discord.Role] = None, role_4: Optional[discord.Role] = None, enabled: bool = True):
    if all(role is None for role in [role_1, role_2, role_3, role_4]) and interaction.guild:
        request = f'SELECT role_1 FROM auto_roles WHERE guild_id = {interaction.guild.id}'
    if interaction.guild and role_1 != None:
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        request = f"SELECT enabled FROM auto_roles WHERE guild_id = {interaction.guild.id}"
        curseur = connexion.cursor()
        curseur.execute(request)
        result = curseur.fetchall()
        print(result)
        if result is not None:
            if result[0][0] == None:
                base_request = "INSERT INTO auto_roles (guild_id, role_1"
                values = [interaction.guild.id, role_1.id]

                base_request_2 = ""
                base_request_3 = ""
                base_request_4 = ""

                request_mid = ", enabled) VALUES (" + ", ".join(map(str, values))
                request_2 = ""
                request_3 = ""
                request_4 = ""
                request_5 = ""
                request_end = ")"

                if role_2 is not None:
                    base_request += ", role_2"
                    values.append(role_2.id)
                    request_2 = f", {role_2.id}"

                if role_3 is not None:
                    base_request += ", role_3"
                    values.append(role_3.id)
                    request_3 = f", {role_3.id}"

                if role_4 is not None:
                    base_request += ", role_4"
                    values.append(role_4.id)
                    request_4 = f", {role_4.id}"

                request = base_request + base_request_2 + base_request_3 + base_request_4 + request_mid + request_2 + request_3 + request_4 + request_5 + request_end

                print(request)

        else:
            base_request = f"UPDATE auto_roles SET role_1 = {role_1.id}"
            values = []

            base_request_2 = ""
            base_request_3 = ""
            base_request_4 = ""

            request_end = f" WHERE guild_id = {interaction.guild.id}"

            if role_2 is not None:
                base_request += f", role_2"
                values.append(role_2.id)
            else:
                base_request += f", role_2 = NULL"

            if role_3 is not None:
                base_request += f", role_3"
                values.append(role_3.id)
            else:
                base_request += f", role_3 = NULL"

            if role_4 is not None:
                base_request += f", role_4"
                values.append(role_4.id)
            else:
                base_request += f", role_4 = NULL"

            if enabled is not None:
                base_request += f", enabled"
                values.append(enabled)
            else:
                base_request += f", enabled = NULL"

            request = base_request + request_end

            print(request)
        curseur.execute(request)
        await interaction.response.send_message("le système d'auto roles pour ce serveur a été configuré avec succès", ephemeral=True)
        # Fermeture de la connexion et commit
        connexion.commit()
        connexion.close()

@client.tree.context_menu(name="Say")
@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
async def say(interaction: discord.Interaction, message: discord.Message):
    if interaction.channel and interaction.channel.type == ChannelType.text:
        await interaction.response.send_modal(ClassModule.Say(message))
        await interaction.channel.typing()

# events
@client.event
async def on_guild_join(guild: discord.Guild):
    if client.user:
        emb = discord.Embed(title="Merci", description=f"Salut, moi c'est {client.user.display_name} ! merci de m'avoir ajoutée au serveur ! je ferai de mon mieux pour répondre à tes attentes.\nsi jamais tu rencontre des problèmes, n'hésite pas à [Ouvrir un ticket](https://github.com/Wishrito/Bread-Chan/issues/new) si tu rencontre un problème !")
        emb.set_author(name=client.user.display_name, icon_url=client.user.display_avatar.url)
        await guild.text_channels[0].send(embed=emb)

@client.event
async def on_member_join(member: discord.Member):
    # DB credentials
    # Connexion à la base de données
    with open('credentials.json', 'r') as fichier:
        donnees_json = json.load(fichier)

    # Connexion à la base de données
    connexion = mysql.connector.connect(**donnees_json)

    select_request = f"SELECT enabled FROM guild_welc WHERE guild_id = {member.guild.id}"
    curseur = connexion.cursor()
    curseur.execute(select_request)
    result = curseur.fetchone()

    if result and bool(result[0]) is True:
        member_name = member.name
        member_display_name = member.display_name
        member_mention = member.mention
        guild_name = member.guild.name
        created_at = member.created_at
        # Use Prepared Statements for SQL Queries
        select_request = f"SELECT welcome_channel_id, welcome_message, img_url FROM guild_welc WHERE guild_id = {member.guild.id}"
        curseur.execute(select_request)
        result = curseur.fetchone()
        MSG = ''
        emb = discord.Embed()
        # Handle Embed Description Properly
        if result is not None:
            if result[1]:
                MSG = result[1]
            if result[2]:
                image_url = result[2]
                emb.set_image(url=image_url)
        emb.description = eval(f"f'{MSG}'")  # Directly assign MSG to emb.description
        channel = None  # Initialize channel as None
        if result:
            if result[0]:
                channel = member.guild.get_channel(result[0])
        if channel and channel.type == ChannelType.text:
            await channel.send(embed=emb)
        select_request = f"SELECT role_1, role_2, role_3, role_4 FROM auto_roles WHERE guild_id = {member.guild.id}"
        curseur.execute(select_request)
        result = curseur.fetchone()
        # Original list
        roleList = [result[0], result[1], result[2], result[3]] if result is not None else []
        # Sublist created with list comprehension
        # Define new sublist that doesn't contain None
        roleList_updated = [value for value in roleList if value is not None]
        for i in roleList_updated:
            await member.add_roles(discord.Object(i))

        connexion.commit()
        connexion.close()   


@client.event
async def on_member_remove(member: discord.Member):
    # DB credentials
    # Connexion à la base de données
    with open('credentials.json', 'r') as fichier:
        donnees_json = json.load(fichier)

    # Connexion à la base de données
    connexion = mysql.connector.connect(**donnees_json)

    select_request = f"SELECT enabled FROM guild_bye WHERE guild_id = {member.guild.id}"
    curseur = connexion.cursor()
    curseur.execute(select_request)
    result = curseur.fetchone()

    if result:
        if bool(result[0]) is True:
            member_name = member.name
            member_display_name = member.display_name
            member_mention = member.mention
            guild_name = member.guild.name
            created_at = member.created_at

            # Use Prepared Statements for SQL Queries
            select_request = f"SELECT goodbye_channel_id, goodbye_message, img_url FROM guild_bye WHERE guild_id = {member.guild.id}"
            curseur.execute(select_request)
            result = curseur.fetchone()
            MSG = ''
            emb = discord.Embed()

            # Handle Embed Description Properly
            if result is not None:
                if result[1]:
                    MSG = result[1]
                if result[2]:
                    image_url = result[2]
                    emb.set_image(url=image_url)


            emb.description = eval(f"f'{MSG}'")  # Directly assign MSG to emb.description
            channel = None  # Initialize channel as None
            if result:
                if result[0]:
                    channel = member.guild.get_channel(result[0])

            if channel and channel.type == ChannelType.text:
                await channel.send(embed=emb)

            connexion.commit()
            connexion.close()   
        else:
            return        

@client.event
async def on_message(message: discord.Message):
    e = message.content.casefold()
    
    async def send_typing_sleep_reply(content: str, sleep_time: float = 1):
        async with message.channel.typing():
            await asyncio.sleep(sleep_time)
        await message.reply(content)

    async def search_regular_str(value: str, string: str):
        phrase = string

        # Utilisation d'une expression régulière pour rechercher le mot "je" en tant que mot distinct
        mot_a_chercher = value
        expression_reguliere = fr"\b{re.escape(mot_a_chercher)}\b"

        if re.search(expression_reguliere, phrase, re.IGNORECASE):
            return True
        else:
            return False

    if client.user and message.author.id != 911467405115535411:
        if await search_regular_str("bite", e) == True:
            await send_typing_sleep_reply("https://cdn.discordapp.com/attachments/778672634387890196/1142544668488368208/nice_cock-1.mp4", 2)

        if await search_regular_str("uwu", e) == True:
            await message.add_reaction("<a:DiscoUwU:1158497203615187015>")

        if await search_regular_str("quoi", e) == True:
            await send_typing_sleep_reply("coubaka! UwU", 1)

        if message.content.startswith(client.user.mention):
            await send_typing_sleep_reply(random.choice(["https://cdn.discordapp.com/attachments/928389065760464946/1131347327416795276/IMG_20210216_162154.png", "src/audio/HORN.mp3"]), 1)

        randcramptes1 = "cramptés ?".casefold()
        randcramptes2 = ["https://didnt-a.sk/", "https://tenor.com/bJniJ.gif", "[ok](https://cdn.discordapp.com/attachments/1139849206308278364/1142583449530683462/videoplayback.mp4)", "[.](https://cdn.discordapp.com/attachments/1130945537907114145/1139100471907336243/Untitled_video_-_Made_with_Clipchamp.mp4)", "tg"]
        for i in range(len(randcramptes1)):
            if e.startswith(f"t'as les {randcramptes1[i]}"):
                await send_typing_sleep_reply(content=random.choice(randcramptes2))

        if ":moyai:" in message.content:
            await message.reply("https://canary.discord.com/store/skus/1037148024792690708/moai")

        word2 = ["https://tiktok.com/", "https://vm.tiktok.com/", "https://www.tiktok.com/"]
        for link in word2:
            if link in message.content:
                vx_tiktok_resolver = str(message.content).replace('https://tiktok.com/', 'https://vxtiktok.com/').replace("https://vm.tiktok.com/","https://vm.vxtiktok.com/").replace("<h","h").replace("> "," ")
                await message.channel.send(content=f"résolution du Tiktok envoyé par {message.author.display_name}[:]({vx_tiktok_resolver})")
                await message.delete()
        if message.guild:
            if message.channel.id == 1190677993434124456 and message.attachments and random.randint(1, 50) == 1:
                await message.add_reaction(random.choice(client.emojis))

            if message.guild.id == 1181845184288411688 and message.channel.type == ChannelType.news:
                await message.publish()

@client.event
async def on_ready():
    if client.user:
        await TasksModule.ReloadPresence.start(client)
        await TasksModule.EpicNotifier.start(client)
        print(f"Connecté en tant que {client.user.name} (ID : {client.user.id})")

        # Chargement des informations de la base de données depuis le fichier JSON
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        # Création des tables si elles n'existent pas déjà
        tables_requests = [
            "CREATE TABLE IF NOT EXISTS user_roles (role_id BIGINT, user_id BIGINT, guild_id BIGINT)",
            "CREATE TABLE IF NOT EXISTS guild_welc (guild_id BIGINT, welcome_channel_id BIGINT, welcome_message VARCHAR(4000), enabled BOOLEAN, img_url VARCHAR(200))",
            "CREATE TABLE IF NOT EXISTS guild_bye (guild_id BIGINT, goodbye_channel_id BIGINT, goodbye_message VARCHAR(4000), enabled BOOLEAN, img_url VARCHAR(200))",
            "CREATE TABLE IF NOT EXISTS auto_roles (guild_id BIGINT, role_1 BIGINT, role_2 BIGINT, role_3 BIGINT, role_4 BIGINT, enabled BOOLEAN)",
            "CREATE TABLE IF NOT EXISTS game_notifier (guild_id BIGINT, epic_games BOOLEAN)"
        ]

        with connexion.cursor() as curseur:
            for request in tables_requests:
                curseur.execute(request)

        # Commit des modifications et fermeture de la connexion
        connexion.commit()
        connexion.close()

client.run(str(risk_var_instance.get_variable_privee()))