import asyncio
import datetime as dat
import json
import os
import random
import re
import sys
from typing import Any, Optional

import discord
import mysql.connector as db
from blagues_api import BlaguesAPI, BlagueType
from discord import ChannelType, Spotify, app_commands
from discord.ext import commands
from discord.gateway import DiscordWebSocket, _log
from discord.permissions import *

import ClassModule
import TasksModule
from ClassModule import SensitveClass
from sysModule import log


# Fonction pour charger les cogs
async def load_cogs():
    # Ajoutez ici tous vos modules de cogs
    cogs = [
        "cog_events",
        "cog_user",
        "cog_role",
        "cog_moderation",
        "cog_support",
        "cog_warframe",
        "cog_admin"
    ]
    for module in cogs:
        cogs_folder = os.path.join(os.path.dirname(__file__), "Cogs")
        if os.path.getsize(os.path.join(cogs_folder, module)) != 0:
            try:
                await client.load_extension(f"Cogs.{module}")
            except Exception as e:
                msg = f"Failed to load {module}: {e}"
            else:
                msg = f"Loaded {module}"
            finally:
                log(msg)

# mobile status


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

# Crée une instance de SensitveClass
sensitiveClass = SensitveClass()


support_guild_id = 1181845184288411688
support_guild = discord.Object(id=support_guild_id)
intents = discord.Intents.all()

roleGroup = app_commands.Group(
    name="role", description="gestion de votre rôle", guild_only=True)
configGroup = app_commands.Group(name="config", description="configuration de systèmes du serveur",
                                 guild_only=True, default_permissions=Permissions(manage_guild=True))
# blagueGroup = app_commands.Group(name="blague", description="système de blagues")

searchGroup = app_commands.Group(
    name="search", description="groupe contenant les différentes commandes de recherche")

# command group for games
# gamegroup = app_commands.Group(name="game", description="group de commandes de jeux")
# genshinGroup = app_commands.Group(parent=gamegroup, name="genshin")
# fortniteGroup = app_commands.Group(parent=gamegroup, name="fortnite")

# discord client def


class BreadChanClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.set_translator(ClassModule.BreadChan_Translator())
        await self.tree.sync(guild=support_guild)
        await self.tree.sync()


def cooldownHandler(interaction: discord.Interaction):
    if interaction.user.id == client.owner_id:
        return None
    else:
        return app_commands.Cooldown(1, 10)


client = BreadChanClient(intents=intents)
emojiGuild = client.get_guild(1001496918343553094)


@client.tree.command(name="ping", description="pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb = discord.Embed(description=f"Pong ! 🏓 {round(client.latency, 1)} ms",
                        color=discord.Color.blurple(), timestamp=dat.datetime.now())
    await interaction.response.send_message(embed=emb, ephemeral=True)


@client.tree.command(name="bot_info", description="permet d'obtenir les infos du bot")
async def botinfo(interaction: discord.Interaction):
    if interaction.client.user:
        emb = discord.Embed()
        emb.author.name = interaction.client.user.display_name
        emb.author.icon_url = interaction.client.user.display_avatar.url
        emb.set_footer(text=interaction.client.user,
                       icon_url=interaction.client.user.avatar)
        emb.add_field(
            name="Imports", value=f"Discord.py : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}\nBlaguesAPI : ?\nPython : {sys.version}", inline=False)
        await interaction.response.send_message(embed=emb, ephemeral=True)


async def help_autocomplete(interaction: discord.Interaction, current: str):
    commandList = [command.name for command in client.tree.walk_commands(
    ) if command.name != 'help' and current.lower() in command.name]
    commandNameList = [
        app_commands.Choice(name=commandName, value=commandName)
        for commandName in commandList if len(commandList) < 25
    ]
    return commandNameList


@client.tree.command(name="help", description="commande d'aide")
@app_commands.autocomplete(command=help_autocomplete)
async def helpCommand(interaction: discord.Interaction, command: Optional[str], ephemeral: bool = True):
    msg = ""
    if not command:
        msg = "serveur de support : https://discord.gg/d6N8urV5pt \ncréer un ticket sur Github : https://github.com/Wishrito/Bread-Chan/issues/new"
    elif client.tree.get_command(command) is not None:
        commande = client.tree.get_command(command)
        if isinstance(commande, app_commands.Group):
            result = [subcommands for subcommands in commande.walk_commands()]
            msg = "cette commande est un groupe de commandes, en voici les commandes détaillées :\n"
            for i in range(len(result)):
                commandeDetails = commande.get_command(result[i].name)
                if isinstance(commandeDetails, app_commands.Command):
                    msg += f"{commandeDetails.qualified_name} : {commandeDetails.description}" + \
                        "\n\n" if i != len(result) else ""
        if isinstance(commande, app_commands.Command):
            msg = f"commande ``{commande.name}`` : {commande.description}"
    else:
        msg = f"commande ``{command}`` introuvable. veuillez réessayer."
    await interaction.response.send_message(msg, ephemeral=ephemeral)


@configGroup.command(name="public", description="voulez vous que le serveur soit public ?")
async def publicGuild(interaction: discord.Interaction, public: Optional[bool]):
    if isinstance(interaction.user, discord.Member) and isinstance(interaction.guild, discord.Guild):
        # DB credentials
        # Connexion à la base de données
        try:
            # Connexion à la base de données
            connexion = db.connect(**sensitiveClass.get_db_credentials())
            curseur = connexion.cursor()
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)
        else:
            if public in [True, False]:
                request = f"UPDATE guild_config SET public = {public} WHERE guild_id = {interaction.guild.id}"
                curseur.execute(request)
                connexion.commit()
                connexion.close()
                await interaction.response.send_message(f"configuration modifié!\n\nPublic : ``{public}``", ephemeral=True)
            elif public is None:
                request = f"SELECT public FROM guild_config WHERE guild_id = {interaction.guild.id}"
                curseur.execute(request)
                result: Any = curseur.fetchone()
                await interaction.response.send_message(f"configuration actuelle :\n\nPublic : ``{bool(result[0])}``", ephemeral=True)
                connexion.close()


async def public_autocomplete(interaction: discord.Interaction, current: str):
    # Connexion à la base de données
    connexion = db.connect(**sensitiveClass.get_db_credentials())
    allowedGuilds: list[str] = []
    for guild in client.guilds:
        request = f"SELECT public FROM guild_config where guild_id = ?"
        curseur = connexion.cursor()
        curseur.execute(request, [guild.id])
        result: Any = curseur.fetchone()
        log(result)
        if result:
            match result[0]:
                case 0:
                    pass
                case 1:
                    allowedGuilds.append(guild.name)
    if allowedGuilds:
        return [
            app_commands.Choice(name=guild_name, value=guild_name)
            for guild_name in allowedGuilds if current in guild_name.casefold()
        ]
    if not allowedGuilds:
        return [
            app_commands.Choice(name="Aucun serveur n'est public", value="con")
        ]
    else:
        return [
            app_commands.Choice(name="???", value='???')
        ]


@client.tree.command(name="random-joke", description="envoie une blague au hasard parmi une sélection")
@app_commands.allowed_contexts(True, True, True)
@app_commands.allowed_installs(True, True)
@app_commands.checks.dynamic_cooldown(cooldownHandler)
async def randJoke(interaction: discord.Interaction):
    blagues = BlaguesAPI(str(sensitiveClass.get_blagues_token()))
    randJoke = await blagues.random()
    await interaction.response.send_message(f"{randJoke.joke}\n\n||{randJoke.answer}||")


@client.tree.command(name="specific-joke", description="envoie une blague d'un type spécifique")
@app_commands.allowed_contexts(True, True, True)
@app_commands.allowed_installs(True, True)
@app_commands.checks.dynamic_cooldown(cooldownHandler)
@app_commands.choices(blaguetype=[app_commands.Choice(name=f"blague {blague.lower()}", value=blague) for blague in dir(BlagueType) if not "__" in blague and blague.isupper()])
async def joke(interaction: discord.Interaction, blaguetype: app_commands.Choice[str]):
    blagues = BlaguesAPI(str(sensitiveClass.get_blagues_token()))
    categorized_joke = await blagues.random_categorized(blaguetype.value.lower())
    await interaction.response.send_message(f"{categorized_joke.joke}\n\n||{categorized_joke.answer}||")


@joke.error
async def jokes_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Commande en cours de recharge. Réessayez dans {error.cooldown.get_retry_after().__round__(2)} secondes.", ephemeral=True)


@randJoke.error
async def randJoke_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Commande en cours de recharge. Réessayez dans {error.cooldown.get_retry_after().__round__(2)} secondes.", ephemeral=True)


@client.tree.command(name="spotify-send-track", description="envoie la musique écouté sur Spotify")
@app_commands.allowed_contexts(True, True, True)
@app_commands.allowed_installs(True, True)
async def spotifyTrack(interaction: discord.Interaction):
    msg = ""
    ephemeral = False
    member = interaction.user.mutual_guilds[0].get_member(interaction.user.id)
    if member:
        spotify_activity = discord.utils.find(
            lambda a: isinstance(a, discord.Spotify), member.activities)
        if isinstance(spotify_activity, Spotify):
            msg = spotify_activity.track_url
        else:
            msg = "Aucune musique en cours d'écoute 🥲"
            ephemeral = True
    else:
        msg = "nous n'avons pas de serveurs en commun, je ne peux donc pas accéder à ce que tu écoutes :("
        ephemeral = True
    await interaction.response.send_message(msg, ephemeral=ephemeral)


@client.tree.command(name="get_partner_invite", description="permet d'obtenir l'accès à un serveur partenaire")
@app_commands.autocomplete(guild=public_autocomplete)
@app_commands.rename(guild="serveur")
async def inviteServ(interaction: discord.Interaction, guild: str):
    gld = discord.utils.get(client.guilds, name=guild)

    if gld is None:
        await interaction.response.send_message("Le serveur spécifié n'a pas été trouvé.", ephemeral=True)
        return

    try:
        timeout = 120
        invited = await gld.text_channels[0].create_invite(max_uses=1, max_age=timeout)
        TimeDelete = dat.datetime.now() + dat.timedelta(seconds=timeout)
        TimeDeleteTotimestamp = round(TimeDelete.timestamp())
        await interaction.response.send_message(f"Voici le lien d'invitation pour \"{guild}\". il expirera dans <t:{TimeDeleteTotimestamp}:R>: {invited}", ephemeral=True)
    except discord.errors.Forbidden:
        await interaction.response.send_message("Je n'ai pas la permission de créer des invitations dans ce serveur.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Une erreur s'est produite : {e}", ephemeral=True)


@configGroup.command(name='word-react', description='Configuration du système de reactions de mots')
async def configWordReact(interaction: discord.Interaction, enabled: Optional[bool]):
    msg = ""
    with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
        json_data = json.load(fichier)

    connexion = db.connect(**json_data)
    curseur = connexion.cursor()
    if interaction.guild:
        if isinstance(enabled, bool):
            curseur.execute(
                f"UPDATE guild_config SET word_react_enabled = {int(enabled)} WHERE guild_id = {interaction.guild.id}")
            msg = f"système de word react activé avec succès !"
            connexion.commit()

        else:
            curseur.execute(
                f"SELECT word_react_enabled FROM guild_config WHERE guild_id = {interaction.guild.id}")
            result: Any = curseur.fetchone()
            if result:
                msg += f"configuration actuelle :\nWord react : ``{result[0]}``"
            else:
                msg += f"hmmm... tu n'etais pas sensé voir ca."

    await interaction.response.send_message(msg, ephemeral=True)

    if connexion:
        curseur.close()
        connexion.close()


@configGroup.command(name="welcome", description="Configuration du système de bienvenue")
@app_commands.rename(option="chat", enabled="activé", img_url="image")
@app_commands.choices(option=[
    app_commands.Choice(name="Salon de bienvenue", value="welcome_ID"),
    app_commands.Choice(name="Message de bienvenue", value="welcome_MSG"),
    app_commands.Choice(name="Définir les deux", value="welcome_ID_&_MSG")
])
async def configWelc(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]] = None, enabled: Optional[bool] = True, img_url: Optional[str] = None):
    if client.user and interaction.guild and client.application:
        owner = client.get_user(client.application.owner.id)
        if isinstance(owner, discord.User):

            # Connexion à la base de données
            connexion = db.connect(**sensitiveClass.get_db_credentials())

            emb = discord.Embed(
                title="config_welcome : configuration actuelle")
            emb.set_author(name=client.user.display_name,
                           url=f"https://discord.com/users/{client.user.id}", icon_url=client.user.display_avatar.url)

            if option == None and enabled == True and img_url == None:
                select_request = f"SELECT welcome_channel_id, welcome_message, enabled, img_url FROM guild_welc where guild_id = {interaction.guild.id}"
                curseur = connexion.cursor()
                curseur.execute(select_request)
                result: Any = curseur.fetchone()
                if result and isinstance(result, tuple):
                    await owner.send(f'result1 = {result}')
                    img = result[3]
                    activated = str(bool(result[2])).replace(
                        'True', 'Oui').replace('False', 'Non')
                    img_txt = " Aucune image de bienvenue n\'a été définie" if str(
                        img) == 'None' else ''
                    channel = interaction.guild.get_channel(result[0])
                    emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
                    log(img)
                    if str(img) != "None":
                        emb.set_image(url=img)
                    await interaction.response.send_message(embed=emb, ephemeral=True)
                else:
                    await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
                curseur.close()
            else:
                style = discord.TextStyle.paragraph
                lenght = 0
                if img_url != None:
                    if "?ex=" in img_url:
                        img_url, buffer = img_url.split("?ex=")

                if option != None and option.value != 'welcome_ID_&_MSG':
                    if option.value == "welcome_ID":
                        lenght = 20
                        style = discord.TextStyle.short
                    elif option.value == "welcome_MSG":
                        lenght = 4000
                        style = discord.TextStyle.long
                    await interaction.response.send_modal(ClassModule.WelcomeModal(option.value, lenght, style, enabled, img_url))
                else:
                    await interaction.response.send_modal(ClassModule.WelcomeModal(option.value if option is not None else "Modal", lenght, style, enabled, img_url))
                await owner.send(f"{option} {enabled} {img_url}")
            connexion.close()


@configGroup.command(name="goodbye", description="Configuration du système de départs")
@app_commands.rename(option="chat", enabled="activé", img_url="image")
@app_commands.choices(option=[
    app_commands.Choice(name="Salon de départ", value="bye_ID"),
    app_commands.Choice(name="Message de départ", value="bye_MSG"),
    app_commands.Choice(name="Définir les deux", value="bye_ID_&_MSG")
])
async def configBye(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]], enabled: Optional[bool], img_url: Optional[str]):
    import ClassModule
    app = interaction.client.application
    if app and interaction.guild and client.user:
        owner = interaction.client.get_user(app.owner.id)
        if isinstance(owner, discord.User):

            # Connexion à la base de données
            connexion = db.connect(**sensitiveClass.get_db_credentials())

            emb = discord.Embed(
                title="config_goodbye : configuration actuelle")
            usr = client.user
            if usr:
                emb.set_author(
                    name=usr.display_name, url=f"https://discord.com/users/{client.user.id}", icon_url=usr.display_avatar.url)

            if option == None and enabled == True and img_url == None:
                select_request = f"SELECT goodbye_channel_id, goodbye_message, enabled, img_url FROM guild_bye where guild_id = {interaction.guild.id}"
                curseur = connexion.cursor()
                curseur.execute(select_request)
                result: Any = curseur.fetchone()
                if result and isinstance(result, tuple):
                    await owner.send(f'result1 = {result}')
                    img = result[3]
                    activated = str(bool(result[2])).replace(
                        'True', 'Oui').replace('False', 'Non')
                    img_txt = " Aucune image de départ n\'a été définie" if str(
                        img) == 'None' else ''
                    if interaction.guild:
                        channel = interaction.guild.get_channel(result[0])
                    emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
                    log(img)
                    if str(img) != "None":
                        emb.set_image(url=img)
                    await interaction.response.send_message(embed=emb, ephemeral=True)
                else:
                    await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
                curseur.close()
            else:
                style = discord.TextStyle.paragraph
                lenght = 0
                if option != None and option.value != 'bye_ID_&_MSG':
                    if option.value == "bye_ID":
                        lenght = 20
                        style = discord.TextStyle.short
                    elif option.value == "bye_MSG":
                        lenght = 4000
                        style = discord.TextStyle.long
                    await interaction.response.send_modal(ClassModule.ByeModal(option.value, lenght, style, enabled, img_url))
                else:
                    await interaction.response.send_modal(ClassModule.ByeModal(option.value if option is not None else "Modal", lenght, style, enabled, img_url))
                await owner.send(f"{option} {enabled} {img_url}")
            connexion.close()


@configGroup.command(name='one-msg-chat', description='configuration du chat autorisant un seul msg')
async def oneMsgChat(interaction: discord.Interaction, channel: Optional[discord.TextChannel], enabled: Optional[bool], role: Optional[discord.Role]):
    if interaction.guild:
        msg = ""
        connexion = db.connect(**sensitiveClass.get_db_credentials())
        cursor = connexion.cursor()
        if all([channel == None, enabled == None, role == None]) == True:
            request = f"SELECT one_msg_channel, one_msg_role_id, one_msg_enabled FROM guild_config WHERE guild_id = {interaction.guild.id}"
            cursor.execute(request)
            result: Any = cursor.fetchone()
            if all([result[0] == 0, result[1] == 0, bool(result[2]) == False]):
                msg = "aucun chat n'a été configuré pour ce système."
            elif interaction.guild:
                unSalon = interaction.guild.get_channel(result[0])
                unRole = interaction.guild.get_role(result[1])
                if unSalon and unRole:

                    msg = f"voici la configuration actuelle :\n\nSalon : {unSalon.mention if result[0] is not None else 'aucun'}\n\nRôle : {unRole.mention if result[1] is not None else 'aucun'}\n\nActivé : {bool(result[2])}"
        else:
            request = f"UPDATE guild_config SET one_msg_channel = {channel.id if channel is not None else 0}, one_msg_enabled = {enabled}, one_msg_role_id = {role.id if role is not None else 0} WHERE guild_id = {interaction.guild.id}"
            try:
                cursor.execute(request)
            except db.DatabaseError as dberr:
                msg = f"une erreur est survenue lors de la connexion à la base de données : {dberr}"
            else:
                if channel:
                    msg = f"la configuration actuelle a été mise à jour !\n\nSalon : {channel.mention}"
        await interaction.response.send_message(msg, ephemeral=True)


@configGroup.command(name="auto-role", description="configuration des rôles automatiques")
async def auto_role_setup(interaction: discord.Interaction, role_1: Optional[discord.Role] = None, role_2: Optional[discord.Role] = None, role_3: Optional[discord.Role] = None, role_4: Optional[discord.Role] = None, enabled: bool = True):
    if all(role is None for role in [role_1, role_2, role_3, role_4]) and interaction.guild:
        request = f'SELECT role_1 FROM auto_roles WHERE guild_id = {interaction.guild.id}'
    if interaction.guild and role_1 != None:

        # Connexion à la base de données
        connexion = db.connect(**sensitiveClass.get_db_credentials())

        request = f"SELECT enabled FROM auto_roles WHERE guild_id = {interaction.guild.id}"
        curseur = connexion.cursor()
        curseur.execute(request)
        result: Any = curseur.fetchall()
        log(result)
        if result:
            if result[0][0] == None:
                base_request = "INSERT INTO auto_roles (guild_id, role_1"
                values = [interaction.guild.id, role_1.id]

                base_request_2 = ""
                base_request_3 = ""
                base_request_4 = ""

                request_mid = ", enabled) VALUES (" + \
                    ", ".join(map(str, values))
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

                request = base_request + base_request_2 + base_request_3 + base_request_4 + \
                    request_mid + request_2 + request_3 + request_4 + request_5 + request_end

                log(request)

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

            log(request)
        try:
            curseur.execute(request)
        except Exception as e:
            log(e)
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


@client.tree.context_menu(name="Profil")
@app_commands.rename(user="Membre")
@app_commands.allowed_installs(True, True)
@app_commands.allowed_contexts(True, True, True)
async def profil(interaction: discord.Interaction, user: discord.Member):
    if client.user:
        # Remove unnecessary characters
        with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
            json_data = json.load(fichier)
        connexion = db.connect(**json_data)
        cursor = connexion.cursor()
        request = f"SELECT user_description FROM user_profile WHERE user_id = {user.id}"
        cursor.execute(request)
        result: Any = cursor.fetchone()
        badges_class = [
            f"{discord.utils.get(client.emojis, name=badge.name)}" for badge in user.public_flags.all()]
        badges = ' '.join(badges_class) if badges_class else "aucun badge"
        if user.accent_color != None:
            log("l'utilisateur a Nitro !")
            badges_class = badges_class.append(discord.utils.get(
                client.emojis, id=1222184055156637726).__str__())
        emb = discord.Embed(title=f"Profil de {user.display_name}", url="https://discord.com/users/{}".format(
            user.id), color=user.color, timestamp=dat.datetime.now())   # Tu peux meme foutre ca en bas, ca precise a quel heure a ete fait l'embed
        emb.add_field(name="Date de création du compte :",
                      value=f"le {discord.utils.format_dt(user.created_at)}")
        if interaction.context.guild:
            emb.add_field(name="Badges :", value=badges)
        if result is not None:
            emb.add_field(name="Description :", value=result[0], inline=False)
        request = f"SELECT user_connexions FROM user_profile WHERE user_id = {user.id}"
        try:
            cursor.execute(request)
            result: Any = cursor.fetchone()
        except db.errors.ProgrammingError as err:
            log(err)
        else:
            if result is not None:
                emb.add_field(name="Connexions :",
                              value=result[0], inline=True)
        # Pour ajouter la pp du type
        emb.set_thumbnail(url=f"{user.display_avatar}")
        # Perso je fous les infos du bot la dessus
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        # type: ignore
        await interaction.response.send_message(embed=emb, ephemeral=True, view=ClassModule.ButtonView(url=user.avatar.url, user=user))
        connexion.commit()
        connexion.close()

# events


@client.event
async def on_guild_join(guild: discord.Guild):
    if client.user:
        for channel in guild.channels:
            if "welcome" in channel.name.casefold() and channel.type == ChannelType.text:
                emb = discord.Embed(
                    title="Merci", description=f"Salut, moi c'est {client.user.display_name} ! merci de m'avoir ajoutée au serveur ! je ferai de mon mieux pour répondre à tes attentes.\nsi jamais tu rencontre des problèmes, n'hésite pas à [Ouvrir un ticket](https://github.com/Wishrito/Bread-Chan/issues/new) si tu rencontre un problème !")
                emb.set_author(name=client.user.display_name,
                               icon_url=client.user.display_avatar.url)
                await channel.send(embed=emb)
                break

    # DB credentials
    # Connexion à la base de données
    with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
        donnees_json = json.load(fichier)

    connexion = db.connect(**sensitiveClass.get_db_credentials())
    curseur = connexion.cursor()
    try:
        # Récupération des noms de toutes les tables dans la base de données "BreadChanDB"
        curseur.execute(
            'SELECT table_name FROM information_schema.tables WHERE table_schema = "BreadChanDB"')
        table_names = curseur.fetchall()
        # Liste des noms de tables à ignorer (comme la table guild_config)
        ignored_tables = ['user_roles']

        # Insertion des guildes dans chaque table prenant en paramètre guild_id
        table_names: Any
        for table in table_names:
            table_name = table[0]
            if table_name not in ignored_tables:
                insert_query = f"INSERT IGNORE INTO {table_name} (guild_id) VALUES ({guild.id})"
                curseur.execute(insert_query)
        connexion.commit()

    except Exception as e:
        log(f"{dat.datetime.now().time()} | Une erreur s'est produite : {str(e)}")
        connexion.rollback()

    finally:
        if connexion:
            connexion.close()
            msg: str | Exception
            channel: discord.abc.GuildChannel
            try:
                breadChanRole = discord.utils.get(
                    guild.roles, name="Bread Chan")
                if breadChanRole:
                    await breadChanRole.edit(color=discord.Colour.orange())
            except discord.errors.HTTPException as discord_err:
                msg = f"une erreur est survenue : {discord_err}"
            else:
                for channel in guild.channels:
                    if "welcome" in channel.name.casefold() and channel.type == ChannelType.text:
                        breadChanRole = discord.utils.get(
                            guild.roles, name='Bread Chan')
                        if breadChanRole:
                            msg = f"je me suis permis de modifier la couleur de mon rôle, {breadChanRole.mention if not None else 'rôle non trouvé'}, j'espère que vous m'en voudrez pas trop 😉"
                        break
            finally:
                if channel.type == ChannelType.text:
                    await channel.send(msg)


@client.event
async def on_member_join(member: discord.Member):
    # DB credentials
    # Connexion à la base de données
    with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
        donnees_json = json.load(fichier)

    # Connexion à la base de données
    connexion = db.connect(**sensitiveClass.get_db_credentials())

    select_request = f"SELECT enabled FROM guild_welc WHERE guild_id = {member.guild.id}"
    curseur = connexion.cursor()
    curseur.execute(select_request)
    results: Any = curseur.fetchone()

    if all([results, bool(results[0]) == True]):
        member_name = member.name
        member_display_name = member.display_name
        member_mention = member.mention
        guild_name = member.guild.name
        created_at = member.created_at
        # Use Prepared Statements for SQL Queries
        select_request = f"SELECT welcome_channel_id, welcome_message, img_url FROM guild_welc WHERE guild_id = {member.guild.id}"
        curseur.execute(select_request)
        results = curseur.fetchone()
        MSG = ''
        emb = discord.Embed()
        channel = None  # Initialize channel as None
        # Handle Embed Description Properly
        if results:
            MSG = results[1]
            if results[2] != None:
                image_url = results[2]
                emb.set_image(url=image_url) if image_url else None
            if results[0]:
                channel = member.guild.get_channel(results[0])

            # Directly assign MSG to emb.description
            emb.description = eval(f"f'{MSG}'")
            if channel and channel != None and channel.type == ChannelType.text:
                await channel.send(embed=emb)
            select_request = f"SELECT role_1, role_2, role_3, role_4 FROM auto_roles WHERE guild_id = {member.guild.id}"
            curseur.execute(select_request)
            results = curseur.fetchone()
            results = tuple(results)
            if results:
                # Original list
                roleList = [result for result in results if result is not None]

                for i in roleList:
                    await member.add_roles(discord.Object(int(i))) if isinstance(i, int) else None

                connexion.commit()
                connexion.close()


@client.event
async def on_member_remove(member: discord.Member):

    # DB credentials
    # Connexion à la base de données
    try:
        connexion = db.connect(**sensitiveClass.get_db_credentials())
    except Exception as e:
        log(e)
    else:
        select_request = f"SELECT enabled FROM guild_bye WHERE guild_id = {member.guild.id}"
        curseur = connexion.cursor()
        curseur.execute(select_request)
        result: Any = curseur.fetchone()

        if result and isinstance(result, tuple):
            if bool(result[0]) is True:
                member_name = member.name
                member_display_name = member.display_name
                member_mention = member.mention
                guild_name = member.guild.name
                created_at = member.created_at

                # Use Prepared Statements for SQL Queries
                select_request = f"SELECT goodbye_channel_id, goodbye_message, img_url FROM guild_bye WHERE guild_id = {member.guild.id}"
                curseur.execute(select_request)
                result: Any = curseur.fetchone()
                MSG = ''
                emb = discord.Embed()

                # Handle Embed Description Properly
                if result and isinstance(result, tuple):
                    if result[1]:
                        MSG = result[1]
                    if result[2]:
                        image_url = result[2]
                        emb.set_image(url=image_url)

                # Directly assign MSG to emb.description
                emb.description = eval(f"f'{MSG}'")
                channel = None  # Initialize channel as None
                if result and isinstance(result, tuple):
                    if result[0]:
                        channel = member.guild.get_channel(result[0])

                if channel and channel.type == ChannelType.text:
                    await channel.send(embed=emb)

                connexion.commit()
                connexion.close()
            else:
                return


client.tree.add_command(roleGroup)
client.tree.add_command(configGroup)
client.tree.add_command(searchGroup)


async def main():
    async with client:
        await load_cogs()
        await client.start(sensitiveClass.get_discord_token())

if __name__ == "__main__":
    asyncio.run(main())
