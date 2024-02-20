import datetime
import os
import re
import discord
from dotenv import load_dotenv
import mysql.connector
import json
from typing import cast, Optional

import requests

class RiskVar:
    def __init__(self):
        pass

    def get_variable_privee(self):
        load_dotenv()
        return os.getenv("discord_token")


class DiscountSetting:
    def __init__(self, discountSetting_data: dict):
        self.dict = discountSetting_data
        self.discountType = discountSetting_data.get('discountType')
        self.discountPercentage = discountSetting_data.get(
            'discountPercentage', '')


class PromotionalOffers:
    def __init__(self, promotionalOffers: dict):
        self.dict = promotionalOffers
        self.startDate: str = promotionalOffers.get('startDate', '')
        self.endDate: str = promotionalOffers.get('endDate', '')
        self.discountSetting = DiscountSetting(
            promotionalOffers.get('discountSetting', ''))

    def __repr__(self):
        return f"{self.dict}"


class Promotions:
    def __init__(self, promotion_data: dict):
        self.dict = promotion_data
        self.promotionalOffers = [PromotionalOffers(
            promotionalOffers_data) for promotionalOffers_data in promotion_data.get('tags', [])]

    def __repr__(self):
        return f"{self.dict}"


class LineOffers:
    def __init__(self, lineOffers_data: dict):
        self.dict = lineOffers_data
        self.appliedRules = lineOffers_data.get('appliedRules', '')

    def __repr__(self):
        return f"{self.dict}"


class FmtPrice:
    def __init__(self, fmtPrice_data: dict):
        self.dict = fmtPrice_data
        self.originalPrice: str = fmtPrice_data.get('originalPrice', '')
        self.discountPrice: str = fmtPrice_data.get('discountPrice', '')
        self.intermediatePrice: str = fmtPrice_data.get(
            'intermediatePrice', '')

    def __repr__(self):
        return f"{self.dict}"


class CurrencyInfo:
    def __init__(self, currencyInfo_data: dict):
        self.dict = currencyInfo_data
        self.decimals: int = currencyInfo_data.get('decimals', '')

    def __repr__(self):
        return f"{self.dict}"


class TotalPrice:
    def __init__(self, totalPrice_data: dict):
        self.dict = totalPrice_data
        self.discountPrice: int = totalPrice_data.get('discountPrice', '')
        self.originalPrice: int = totalPrice_data.get('originalPrice', '')
        self.voucherDiscount: int = totalPrice_data.get('voucherDiscount', '')
        self.discount: int = totalPrice_data.get('discount', '')
        self.currencyCode: str = totalPrice_data.get('currencyCode', '')
        self.currencyInfo = CurrencyInfo(
            totalPrice_data.get('currencyInfo', ''))
        self.fmtPrice = FmtPrice(totalPrice_data.get('fmtPrice', ''))

    def __repr__(self):
        return f"{self.dict}"


class Price:
    def __init__(self, price_data: dict):
        self.dict = price_data
        self.totalPrice = TotalPrice(price_data.get('totalPrice', ''))
        self.lineOffers = [LineOffers(
            lineOffers_data) for lineOffers_data in price_data.get('tags', [])]

    def __repr__(self):
        return f"{self.dict}"


class Mappings:
    def __init__(self, mappings_data: dict):
        self.dict = mappings_data
        self.pageSlug: str = mappings_data.get('pageSlug', '')
        self.pageType: str = mappings_data.get('pageType', '')

    def __repr__(self):
        return f"{self.dict}"


class CatalogNs:
    def __init__(self, catalogNs_data: dict):
        self.dict: dict = catalogNs_data
        self.mappings = catalogNs_data.get('mappings', '')

    def __repr__(self):
        return f"{self.dict}"


class Tags:
    def __init__(self, tags_data: dict):
        self.dict: dict = tags_data
        self.id: str = tags_data.get('id', '')

    def __repr__(self):
        return f"{self.dict}"


class Categories:
    def __init__(self, categories_data: dict):
        self.dict: dict = categories_data
        self.path: str = categories_data.get('path', '')

    def __repr__(self):
        return f"{self.dict}"


class CustomAttributes:
    def __init__(self, attributes_data: dict):
        self.dict: dict = attributes_data
        self.key: str = attributes_data.get('key', '')
        self.value: str = attributes_data.get('value', '')

    def __repr__(self):
        return f"{self.dict}"


class Items:
    def __init__(self, item_data: dict):
        self.dict: dict = item_data
        self.id: int = item_data.get('id', '')
        self.namespace: str = item_data.get('namespace', '')

    def __repr__(self):
        return f"{self.dict}"


class KeyImage:
    def __init__(self, image_data: dict):
        self.dict: dict = image_data
        self.type: str = image_data.get('type', '')
        self.url: str = image_data.get('url', '')

    def __repr__(self):
        return f"{self.dict}"


class Seller:
    def __init__(self, seller_data: dict):
        self.dict: dict = seller_data
        self.id: int = seller_data.get('id', '')
        self.name: str = seller_data.get('name', '')

    def __repr__(self):
        return f"{self.dict}"


class Game:
    def __init__(self, game_data: dict):
        self.dict: dict = game_data
        self.name: str = game_data.get('title', '')
        self.id: int = game_data.get('id', '')
        self.description: str = game_data.get('description', '')
        self.url: str = game_data.get('url', '')
        self.namespace: str = game_data.get('namespace', '')
        self.effectiveDate: str = game_data.get('effectiveDate', '')
        self.offerType: str = game_data.get('offerType', '')
        self.expiryDate: str = game_data.get('expiryDate', '')
        self.viewableDate: str = game_data.get('viewableDate', '')
        self.status: str = game_data.get('status', '')
        self.isCodeRedemptionOnly: bool = bool(game_data.get(
            'isCodeRedemptionOnly', ''))
        self.keyImages = [KeyImage(image_data)
                          for image_data in game_data.get('keyImages', [])]
        self.seller = Seller(game_data.get('seller', ''))
        self.productSlug: str = game_data.get('productSlug', '')
        self.urlSlug: str = game_data.get('urlSlug', '')
        self.url: str = game_data.get('url', '')
        self.items = [Items(item_data)
                      for item_data in game_data.get('items', [])]
        self.customAttributes = [CustomAttributes(
            customAttributes_data) for customAttributes_data in game_data.get('customAttributes', [])]
        self.categories = [Categories(
            categories_data) for categories_data in game_data.get('categories', [])]
        self.tags = [Tags(
            tags_data) for tags_data in game_data.get('tags', [])]
        self.catalogNs = CatalogNs(game_data.get('catalogNs', ''))
        self.price = Price(game_data.get('price', ''))
        self.promotions = Promotions(game_data.get('promotions', ''))

    def __repr__(self):
        return f"{self.dict}"


class EpicBaseClass:
    def __init__(self):
        url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"
        request = requests.get(url)
        self.games: list[Game] = []
        self.process_json_data(dict(request.json()))
        self.request = request

    def process_json_data(self, json_data: dict):
        """System class : do not use"""
        if 'data' in json_data and 'Catalog' in json_data['data'] and 'searchStore' in json_data['data']['Catalog']:
            elements = json_data['data']['Catalog']['searchStore']['elements']
            for element in elements:
                game_instance = Game(element)
                self.games.append(game_instance)

    def get_next_free_game(self):
        json_data = self.request.json()
        if 'data' in json_data and 'Catalog' in json_data['data'] and 'searchStore' in json_data['data']['Catalog']:
            elements = json_data['data']['Catalog']['searchStore']['elements']

            # Obtenez la date actuelle
            current_date = datetime.datetime.now()

            # Initialisez la date la plus proche avec une date arbitrairement grande
            closest_date = datetime.datetime.max

            # Parcourez votre liste de dates
            for element in range(elements):
                # Convertissez la date de la liste en objet datetime
                epic_instance = EpicBaseClass()
                list_date = datetime.datetime.strptime(
                    epic_instance.games[element].promotions.promotionalOffers[0].endDate, '%Y-%m-%dT%H:%M:%S.%fZ')

                # Vérifiez si la date de la liste est plus proche de la date actuelle que la date la plus proche actuelle
                if list_date > current_date and list_date < closest_date:
                    closest_date = list_date
                return


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
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

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
            self.add_item(discord.ui.TextInput(label='bye_ID', max_length=20, style=discord.TextStyle.short))
            self.add_item(discord.ui.TextInput(label='bye_MSG', placeholder="{member_name} | {member_display_name} | {member_mention} | {guild_name} | {created_at}", max_length=4000, style=discord.TextStyle.long))
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
        with open('credentials.json', 'r') as fichier:
            donnees_json = json.load(fichier)

        # Connexion à la base de données
        connexion = mysql.connector.connect(**donnees_json)

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
                    insert_request = f"INSERT INTO guild_bye (guild_id, goodbye_channel_id, enabled, img_url) VALUES ({interaction.guild.id}, {value}, {self.enabled}, \"{self.image_url}\")"
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

# class Dropdown(discord.ui.Select):
#     def __init__(self, data):
#         self.data = data
#         # définis les options qui seront affichées dans le dropdown
#         options=[]
#         for char in self.data.characters:
#             self.char = char
#             options.append(discord.SelectOption(label=char.name, description=f"le build de {char.name}", value=char.name.lower())) # add dropdown option for each character in data.character
#             super().__init__(placeholder="Sélectionne le build que tu souhaite regarder :", min_values=1, max_values=1, options=options)
#         # The placeholder is what will be shown when no option is chosen
#         # The min and max values indicate we can only pick one of the three options
#         # The options parameter defines the dropdown options. We defined this above
#     async def callback(self, interaction: discord.Interaction):
#         # Use the interaction object to send a response message containing
#         # the user's favourite colour or choice. The self object refers to the
#         # Select object, and the values attribute gets a list of the user's
#         # selected options. We only want the first one.
#         emb=discord.Embed(title=f"{self.data.player.nickname}'s {self.values[0].title()}", description=f"Voici les informations du personnage:\n\ncrit rate:", color = discord.Color.green(), timestamp=datetime.datetime.now())
#         emb.set_author(name=f"{client.user}", icon_url=f"{self.data.player.avatar.icon.url}", url=f"https://enka.network/u/{self.data.uid}")
#         emb.set_footer(text=f"{interaction.user.name}", icon_url=interaction.guild.icon) #type: ignore
#         await interaction.response.send_message(f"Voici le build de {self.values[0].title()}:", ephemeral=True, embed=emb)

# class DropdownView(discord.ui.View):
#     def __init__(self, data):
#         super().__init__(timeout=float(10))
#         self.data = data
#         # Adds the dropdown to our view object.
#         self.add_item(Dropdown(data))
