import datetime as dat
import os
import re
import discord
from discord import app_commands, Locale
from discord.ext import commands
from dotenv import load_dotenv
import mysql.connector as db
from googletrans import Translator
from googletrans.models import Translated

import json
from typing import Any, Union, cast, Optional

from sysModule import log


class BreadChan_Translator(app_commands.Translator):
    translator = Translator()
    ignore_translate = ['…']  # expand if necessary

    async def translate(self, string: app_commands.locale_str, locale: Locale, context: app_commands.TranslationContext) -> str | None:
        if locale is Union[Locale.american_english, Locale.british_english]:  # check user's locale
            if string.message in self.ignore_translate:
                pass
            else:
                try:
                    if '-' in locale.value:
                        # pour garder uniquement les deux premières lettres du code
                        outputLangCode = locale.value.split('-')[0]
                    else:
                        outputLangCode = locale.value  # pour garder le même code que celui par défaut
                    translated = self.translator.translate(
                        string, dest=outputLangCode)
                except Exception as e:
                    log(e)
                    pass
                else:
                    if isinstance(translated, Translated):
                        if string.message != translated.text:
                            log(
                                f"translated from \"{string.message}\" to \"{translated.text}\"")
                            return translated.text
                        else:
                            pass
        else:
            pass


class SensitveClass:
    def __init__(self):
        pass

    def get_discord_token(self) -> str:
        load_dotenv()
        DISCORD_TOKEN = os.getenv("discord_token")
        return DISCORD_TOKEN if DISCORD_TOKEN is not None else ''

    def get_blagues_token(self) -> str | None:
        load_dotenv()
        BLAGUES_TOKEN = os.getenv("blagues_api_token")
        if BLAGUES_TOKEN is None:
            return None
        return BLAGUES_TOKEN

    def get_db_credentials(self) -> Any:
        load_dotenv()
        CREDENTIALS = {
            "host": os.getenv("db_host"),
            "user": os.getenv("db_user"),
            "password": os.getenv("db_password"),
            "database": os.getenv("db_name")
        }
        if None in CREDENTIALS:
            return None
        return CREDENTIALS

    def initialize_db(self, client: commands.Bot):
        # Connexion à la base de données
        try:
            connexion = db.connect(**sensitiveClass.get_db_credentials())
        except db.Error as e:
            log(e)
        else:
            # Création des tables si elles n'existent pas déjà
            tables_requests = [
                "CREATE TABLE IF NOT EXISTS user_roles (role_id BIGINT PRIMARY KEY, user_id BIGINT, guild_id BIGINT, FOREIGN KEY (guild_id) REFERENCES guild_config(guild_id))",
                "CREATE TABLE IF NOT EXISTS guild_welc (guild_id BIGINT PRIMARY KEY, welcome_channel_id BIGINT, welcome_message VARCHAR(4000) NOT NULL DEFAULT 'Bienvenue sur {server_name} {member_name} !', enabled BOOLEAN NOT NULL DEFAULT FALSE, img_url VARCHAR(200), FOREIGN KEY (guild_id) REFERENCES guild_config(guild_id))",
                "CREATE TABLE IF NOT EXISTS guild_bye (guild_id BIGINT PRIMARY KEY, goodbye_channel_id BIGINT, goodbye_message VARCHAR(4000) NOT NULL DEFAULT '{member_name} a quitté le serveur, au revoir !', enabled BOOLEAN NOT NULL DEFAULT FALSE, img_url VARCHAR(200), FOREIGN KEY (guild_id) REFERENCES guild_config(guild_id))",
                "CREATE TABLE IF NOT EXISTS auto_roles (guild_id BIGINT PRIMARY KEY, role_1 BIGINT, role_2 BIGINT, role_3 BIGINT, role_4 BIGINT, enabled BOOLEAN NOT NULL DEFAULT FALSE, FOREIGN KEY (guild_id) REFERENCES guild_config(guild_id))",
                "CREATE TABLE IF NOT EXISTS epic_game_notifier (guild_id BIGINT PRIMARY KEY, enabled BOOLEAN NOT NULL DEFAULT FALSE, FOREIGN KEY (guild_id) REFERENCES guild_config(guild_id))",
                "CREATE TABLE IF NOT EXISTS guild_config (guild_id BIGINT PRIMARY KEY, public BOOLEAN NOT NULL DEFAULT FALSE, word_react_enabled BOOLEAN NOT NULL DEFAULT FALSE, auto_post_enabled BOOLEAN NOT NULL DEFAULT FALSE, auto_post_channel BIGINT, one_msg_role_id BIGINT NOT NULL DEFAULT 0, one_msg_channel BOOLEAN NOT NULL DEFAULT 0)",
                "CREATE TABLE IF NOT EXISTS wm_credentials (user_id BIGINT NOT NULL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL);"
            ]

            curseur = connexion.cursor()
            guild_ids = [(guild.id,) for guild in client.guilds]
            try:
                # Création des tables
                for request in tables_requests:
                    curseur.execute(request)
                connexion.commit()

                # Récupération des noms de toutes les tables dans la base de données "BreadChanDB"
                curseur.execute(
                    'SELECT table_name FROM information_schema.tables WHERE table_schema = "BreadChanDB"')
                table_names: Any = curseur.fetchall()

                # Liste des noms de tables à ignorer (comme la table guild_config)
                ignored_tables = ['user_roles', 'guild_roles_type',
                                  'guild_roles_mod', "user_profile"]

                # Insertion des guildes dans chaque table prenant en paramètre guild_id
                for table in table_names:
                    table_name = table[0]
                    if table_name not in ignored_tables:
                        insert_query = f"INSERT IGNORE INTO {table_name} (guild_id) VALUES (%s)"
                        curseur.executemany(insert_query, guild_ids)
                connexion.commit()

            except Exception as e:
                log(e)
                connexion.rollback()

            finally:
                if connexion:
                    connexion.close()


sensitiveClass = SensitveClass()


class LoginModal(discord.ui.Modal):
    def __init__(self, title: str = "Formulaire"):
        self.title = title
        super().__init__()
    mailInput = discord.ui.TextInput(
        style=discord.TextStyle.long, label="e-mail")
    pwdInput = discord.ui.TextInput(
        style=discord.TextStyle.long, label="Mot de Passe")

    async def on_submit(self, interaction: discord.Interaction):

        connexion = db.connect(**sensitiveClass.get_db_credentials())
        cursor = connexion.cursor()
        # Insertion des identifiants dans la base de données
        cursor.execute('''
            INSERT INTO wm_credentials (user_id, email, password)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            warframe_username = VALUES(warframe_username),
            warframe_password = VALUES(warframe_password)
        ''', (interaction.user.id, self.mailInput.value, self.pwdInput.value))
        connexion.commit()
        connexion.close()


class Say(discord.ui.Modal, title="contenu du reply"):
    def __init__(self, msg: discord.Message):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(
        style=discord.TextStyle.paragraph, label="Texte", min_length=1)
    ping = discord.ui.TextInput(style=discord.TextStyle.short, label="Mention",
                                min_length=3, max_length=3, placeholder="Oui ou Non", required=False)
    ping2 = bool(ping.value.casefold().replace(
        "oui", "True").replace("non", "False"))

    async def on_submit(self, interaction: discord.Interaction):
        if not self.ping:
            await self.msg.reply(self.textinput.value, mention_author=True)
            await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)
        else:
            await self.msg.reply(self.textinput.value, mention_author=self.ping2)
            await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)


class WelcomeModal(discord.ui.Modal):
    def __init__(self, label: str, lenght:  Optional[int], style: Optional[discord.TextStyle], enabled: Optional[bool], image_url: Optional[str]):
        super().__init__(title=f"Paramétrage : {label}")

        self.label = label
        self.lenght = lenght
        self.style = style
        self.enabled = enabled
        self.image_url = image_url
        if self.label == 'welcome_ID_&_MSG':
            self.add_item(discord.ui.TextInput(label='welcome_ID',
                          max_length=20, style=discord.TextStyle.short))
            self.add_item(discord.ui.TextInput(
                label='welcome_MSG', placeholder="{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}", max_length=4000, style=discord.TextStyle.long))
        else:
            self.add_item(discord.ui.TextInput(label=label, max_length=lenght,
                          style=style if style is not None else discord.TextStyle.paragraph))
            input = cast(discord.ui.TextInput, self.children[0])
            if input.label == 'welcome_MSG':
                input.placeholder = "{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}"
            else:
                return

    async def on_submit(self, interaction: discord.Interaction):
        # DB credentials
        # Connexion à la base de données
        with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = db.connect(**sensitiveClass.get_db_credentials())

        value = cast(discord.ui.TextInput, self.children[0]).value
        insert_request = ''
        curseur = connexion.cursor()
        if interaction.guild:
            if self.label == 'welcome_ID':
                channel_id = int(value)
                channel = interaction.guild.get_channel(channel_id)
                select_request = f"SELECT welcome_channel_id FROM guild_welc WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                id_welcome = curseur.fetchone()
                if id_welcome:
                    insert_request = f"UPDATE guild_welc SET"

                    if value is not None:
                        insert_request += f" welcome_channel_id = {value},"

                    if self.enabled is not None:
                        insert_request += f" enabled = {self.enabled},"

                    if self.image_url is not None:
                        insert_request += f" img_url = \"{self.image_url}\","

                    # Supprimer la virgule finale si des modifications ont été apportées
                    if insert_request.endswith(","):
                        insert_request = insert_request[:-1]

                    insert_request += f" WHERE guild_id = {interaction.guild.id}"
                else:
                    insert_request = "INSERT INTO guild_welc (guild_id"

                    values: list[int | str | bool] = [interaction.guild.id]

                    if value is not None:
                        insert_request += ", welcome_channel_id"
                        values.append(value)

                    if self.enabled is not None:
                        insert_request += ", enabled"
                        values.append(self.enabled)

                    if self.image_url is not None:
                        insert_request += ", img_url"
                        values.append(f"\"{self.image_url}\"")

                    insert_request += ") VALUES (" + \
                        ", ".join(map(str, values)) + ")"
            if channel:
                await interaction.response.send_message(f"le salon {channel.mention} est désormais le salon d'annonces de nouveau membre sur ce serveur.", ephemeral=True)

            if self.label == 'welcome_MSG':
                msg_welcome = value
                select_request = f"SELECT welcome_channel_id FROM guild_welc WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                msg_welcome = curseur.fetchone()
                if msg_welcome:
                    insert_request = f"UPDATE guild_welc SET welcome_message = \"{value}\", enabled = {self.enabled}, img_url = \"{self.image_url}\"  WHERE guild_id = {interaction.guild.id}"
                else:
                    insert_request = f"INSERT INTO guild_welc (guild_id, welcome_message, enabled, img_url) VALUES ({interaction.guild.id}, \"{value}\", {self.enabled}, \"{self.image_url}\")"
                await interaction.response.send_message(f"le message de bienvenue est désormais le suivant sur ce serveur:\n\n{value}", ephemeral=True)
                curseur.execute(
                    insert_request) if insert_request != '' else None

            if self.label == 'welcome_ID_&_MSG':
                value_ID = cast(discord.ui.TextInput, self.children[0]).value
                value_MSG = cast(discord.ui.TextInput, self.children[1]).value
                select_request = f"SELECT welcome_channel_id, welcome_message, img_url FROM guild_welc WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                msg_ID_welcome = curseur.fetchone()

                requests = []
                for index, value in enumerate([value_ID, value_MSG, self.image_url]):
                    if msg_ID_welcome[index] is not None:  # type: ignore
                        if index == 0:
                            requests.append(
                                f"UPDATE guild_welc SET welcome_channel_id = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")
                        elif index == 1:
                            requests.append(
                                f"UPDATE guild_welc SET welcome_message = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")
                        elif index == 2:
                            requests.append(
                                f"UPDATE guild_welc SET img_url = \"{value}\" WHERE guild_id = {interaction.guild.id}")

                if msg_ID_welcome is None:
                    requests = f"INSERT INTO guild_welc (guild_id, welcome_channel_id, welcome_message, enabled, img_url) VALUES ({interaction.guild.id}, {value_ID} , \"{value_MSG}\", {self.enabled}, \"{self.image_url}\")"

                channel = interaction.guild.get_channel(int(value_ID))
                if channel is not None:
                    await interaction.response.send_message(f"le message de bienvenue est désormais le suivant sur ce serveur : {value_MSG}\n\nLe salon des annonces de nouveaux membres est le suivant : {channel.mention}", ephemeral=True)
                for i in requests:
                    curseur.execute(i)
            # Fermeture de la connexion et commit
            connexion.commit()
            connexion.close()


class ByeModal(discord.ui.Modal):
    def __init__(self, label: str, lenght:  Optional[int], style: Optional[discord.TextStyle], enabled: Optional[bool], image_url: Optional[str]):
        super().__init__(title=f"Paramétrage : {label}")

        self.label = label
        self.lenght = lenght
        self.style = style
        self.enabled = enabled
        self.image_url = image_url
        if self.label == 'bye_ID_&_MSG':
            self.add_item(discord.ui.TextInput(label='bye_ID',
                          max_length=20, style=discord.TextStyle.short))
            self.add_item(discord.ui.TextInput(
                label='bye_MSG', placeholder="{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}", max_length=4000, style=discord.TextStyle.long))
        else:
            self.add_item(discord.ui.TextInput(label=label, max_length=lenght,
                          style=style if style is not None else discord.TextStyle.long))
            input = cast(discord.ui.TextInput, self.children[0])
            if input.label == 'bye_MSG':
                input.placeholder = "{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}"
            else:
                return

    async def on_submit(self, interaction: discord.Interaction):
        # DB credentials
        # Connexion à la base de données
        with open(os.path.join(os.path.dirname(__file__), './credentials.json'), 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = db.connect(**sensitiveClass.get_db_credentials())

        value = cast(discord.ui.TextInput, self.children[0]).value
        insert_request = ''
        curseur = connexion.cursor()
        if interaction.guild:
            if self.label == 'welcome_ID':
                channel_id = int(value)
                channel = interaction.guild.get_channel(channel_id)
                select_request = f"SELECT goodbye_channel_id FROM guild_bye WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                id_bye = curseur.fetchone()
                if not id_bye:
                    insert_request = f"INSERT INTO guild_bye (guild_id," + " goodbye_channel_id" if value is not None else "" + ", enabled" if self.enabled is not None else "" + ", img_url" + \
                        f") VALUES ({interaction.guild.id}" + f", {value}" if value is not None else "" + \
                        f", {self.enabled}" if self.enabled is not None else "" + \
                        f", \"{self.image_url if self.image_url else None}\")"
                if id_bye:
                    insert_request = f"UPDATE guild_bye SET goodbye_channel_id = {value}, enabled = {self.enabled}, img_url = \"{self.image_url}\" WHERE guild_id = {interaction.guild.id}"
                if channel:
                    await interaction.response.send_message(f"le salon {channel.mention} est désormais le salon d'annonces de départ de membres sur ce serveur.", ephemeral=True)

            if self.label == 'bye_MSG':
                msg_bye = value
                select_request = f"SELECT goodbye_channel_id FROM guild_bye WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                msg_bye = curseur.fetchone()
                if not msg_bye:
                    insert_request = f"INSERT INTO guild_bye (guild_id, goodbye_message, enabled, img_url) VALUES ({interaction.guild.id}, \"{value}\", {self.enabled}, \"{self.image_url}\")"
                else:
                    insert_request = f"UPDATE guild_bye SET goodbye_message = \"{value}\", enabled = {self.enabled}, img_url = \"{self.image_url}\"  WHERE guild_id = {interaction.guild.id}"

                await interaction.response.send_message(f"le message de bienvenue est désormais le suivant sur ce serveur:\r\r{value}", ephemeral=True)

            if self.label == 'bye_ID_&_MSG':
                value_ID = cast(discord.ui.TextInput, self.children[0]).value
                value_MSG = cast(discord.ui.TextInput, self.children[1]).value
                select_request = f"SELECT goodbye_channel_id, goodbye_message, img_url FROM guild_bye WHERE guild_id = {interaction.guild.id}"
                curseur.execute(select_request)
                msg_ID_welcome = curseur.fetchone()

                requests = []

                if msg_ID_welcome is not None:
                    update_columns = ["goodbye_channel_id",
                                      "goodbye_message", "img_url"]
                    for index, value in enumerate([value_ID, value_MSG, self.image_url]):
                        if msg_ID_welcome[index]:
                            column = update_columns[index]
                            requests.append(
                                f"UPDATE guild_bye SET {column} = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")

                    for i in requests:
                        curseur.execute(i)

                elif msg_ID_welcome is None:
                    insert_request = f"INSERT INTO guild_bye (guild_id, goodbye_channel_id, goodbye_message, enabled, img_url) VALUES ({interaction.guild.id}, {value_ID} , \"{value_MSG}\", {self.enabled}, \"{self.image_url}\")"

                channel = interaction.guild.get_channel(int(value_ID))
                if channel:
                    await interaction.response.send_message(f"le message de départ est désormais le suivant sur ce serveur : {value_MSG}\n\nLe salon des annonces de départ de membres est le suivant : {channel.mention}", ephemeral=True)

            curseur.execute(insert_request)
            # Fermeture de la connexion et commit
            connexion.commit()
            connexion.close()


class ButtonView(discord.ui.View):
    def __init__(self, url: str, user: discord.User, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.url,
                      label=f"Photo de profil de {user.name}", url=url))
