import datetime
import os
import discord
from dotenv import load_dotenv
import mysql.connector
import json
from typing import cast, Optional

class RiskVar:
    def __init__(self):
        pass

    def get_variable_privee(self):
        load_dotenv()
        return os.getenv("discord_token")

class Say(discord.ui.Modal, title="contenu du reply"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(style=discord.TextStyle.paragraph, label="Texte", min_length=1)
    ping = discord.ui.TextInput(style=discord.TextStyle.short, label="Mention", min_length=3, max_length=3, placeholder="Oui ou Non", required=False)
    ping2 = bool(ping.value.casefold().replace("oui", "True").replace("non", "False"))
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
            self.add_item(discord.ui.TextInput(label='welcome_ID', max_length=20, style=discord.TextStyle.short))
            self.add_item(discord.ui.TextInput(label='welcome_MSG', placeholder="{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}", max_length=4000, style=discord.TextStyle.long))
        else:
            self.add_item(discord.ui.TextInput(label=label, max_length=lenght, style=style))
            input = cast(discord.ui.TextInput, self.children[0])
            if input.label == 'welcome_MSG':
                input.placeholder = "{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}"
            else:
                return
    async def on_submit(self, interaction: discord.Interaction):
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        value = cast(discord.ui.TextInput, self.children[0]).value
        insert_request = ''
        curseur = connexion.cursor()
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
                
                insert_request += ") VALUES (" + ", ".join(map(str, values)) + ")"

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
        curseur.execute(insert_request) if insert_request != '' else None

        if self.label == 'welcome_ID_&_MSG':
            value_ID = cast(discord.ui.TextInput, self.children[0]).value
            value_MSG = cast(discord.ui.TextInput, self.children[1]).value
            select_request = f"SELECT welcome_channel_id, welcome_message, img_url FROM guild_welc WHERE guild_id = {interaction.guild.id}"
            curseur.execute(select_request)
            msg_ID_welcome = curseur.fetchone()

            requests = []
            for index, value in enumerate([value_ID, value_MSG, self.image_url]):
                if msg_ID_welcome[index] is not None:
                    if index == 0:
                        requests.append(f"UPDATE guild_welc SET welcome_channel_id = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")
                    elif index == 1:
                        requests.append(f"UPDATE guild_welc SET welcome_message = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")
                    elif index == 2:
                        requests.append(f"UPDATE guild_welc SET img_url = \"{value}\" WHERE guild_id = {interaction.guild.id}")

            if msg_ID_welcome is None:
                requests = f"INSERT INTO guild_welc (guild_id, welcome_channel_id, welcome_message, enabled, img_url) VALUES ({interaction.guild.id}, {value_ID} , \"{value_MSG}\", {self.enabled}, \"{self.image_url}\")"
            
            channel = interaction.guild.get_channel(int(value_ID))
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
            self.add_item(discord.ui.TextInput(label='bye_ID', max_length=20, style=discord.TextStyle.short))
            self.add_item(discord.ui.TextInput(label='bye_MSG', placeholder="{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}", max_length=4000, style=discord.TextStyle.long))
        else:
            self.add_item(discord.ui.TextInput(label=label, max_length=lenght, style=style))
            input = cast(discord.ui.TextInput, self.children[0])
            if input.label == 'bye_MSG':
                input.placeholder = "{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}"
            else:
                return
    async def on_submit(self, interaction: discord.Interaction):
        # DB credentials
        # Connexion à la base de données
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

        value = cast(discord.ui.TextInput, self.children[0]).value
        insert_request = ''
        curseur = connexion.cursor()
        if self.label == 'welcome_ID':
            channel_id = int(value)
            channel = interaction.guild.get_channel(channel_id)
            select_request = f"SELECT goodbye_channel_id FROM guild_bye WHERE guild_id = {interaction.guild.id}"
            curseur.execute(select_request)
            id_bye = curseur.fetchone()
            if not id_bye:
                insert_request = f"INSERT INTO guild_bye (guild_id, goodbye_channel_id, enabled, img_url) VALUES ({interaction.guild.id}, {value}, {self.enabled}, \"{self.image_url}\")"
            else:
                insert_request = f"UPDATE guild_bye SET goodbye_channel_id = {value}, enabled = {self.enabled}, img_url = \"{self.image_url}\" WHERE guild_id = {interaction.guild.id}"
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
                update_columns = ["goodbye_channel_id", "goodbye_message", "img_url"]
                for index, value in enumerate([value_ID, value_MSG, self.image_url]):
                    if msg_ID_welcome[index]:
                        column = update_columns[index]
                        requests.append(f"UPDATE guild_bye SET {column} = \"{value}\", enabled = {self.enabled} WHERE guild_id = {interaction.guild.id}")


                for i in requests:
                    curseur.execute(i)

            elif msg_ID_welcome is None:
                insert_request = f"INSERT INTO guild_bye (guild_id, goodbye_channel_id, goodbye_message, enabled, img_url) VALUES ({interaction.guild.id}, {value_ID} , \"{value_MSG}\", {self.enabled}, \"{self.image_url}\")"
            
            channel = interaction.guild.get_channel(int(value_ID))
            await interaction.response.send_message(f"le message de départ est désormais le suivant sur ce serveur : {value_MSG}\n\nLe salon des annonces de départ de membres est le suivant : {channel.mention}", ephemeral=True)

        curseur.execute(insert_request)
        # Fermeture de la connexion et commit
        connexion.commit()
        connexion.close()

class Dropdown(discord.ui.Select):
    def __init__(self, data):
        self.data = data
        # définis les options qui seront affichées dans le dropdown
        options=[]
        for char in self.data.characters:
            self.char = char
            options.append(discord.SelectOption(label=char.name, description=f"le build de {char.name}", value=char.name.lower())) # add dropdown option for each character in data.character
            super().__init__(placeholder="Sélectionne le build que tu souhaite regarder :", min_values=1, max_values=1, options=options)
        # The placeholder is what will be shown when no option is chosen 
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        emb=discord.Embed(title=f"{self.data.player.nickname}'s {self.values[0].title()}", description=f"Voici les informations du personnage:\n\ncrit rate:", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", icon_url=f"{self.data.player.avatar.icon.url}", url=f"https://enka.network/u/{self.data.uid}")
        emb.set_footer(text=f"{interaction.user.name}", icon_url=interaction.guild.icon) #type: ignore     
        await interaction.response.send_message(f"Voici le build de {self.values[0].title()}:", ephemeral=True, embed=emb)
        
class DropdownView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=float(10))
        self.data = data
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(data))