#Import des libs python de base
import os, sys
import datetime
import random
from dotenv import load_dotenv
from typing import List, Optional
from io import BytesIO
import asyncio
from collections import * #type: ignore

#Import de discord et modules discord
import discord
import discord.ext.commands
from discord import ButtonStyle, app_commands, Team, ui
from discord.ext import tasks
from discord.gateway import DiscordWebSocket, _log
from discord.utils import MISSING
from requests import request
import moderation

#Import des API
import unbelipy as unb
import blagues_api as bl
import brawlstats as brst
import other_functions
import enkanetwork as enk
import fortnite_api as ftn
from fortnite_api import errors
from rule34Py import rule34Py
import openai

#Import de PIL
from PIL import Image, ImageDraw, ImageFont

#Import de win10toast
from win10toast import ToastNotifier

import sqlite3



#paramètres

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

# tokens
load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")
BLAGUES_TOKEN = os.getenv("blagues_api_token")
BS_TOKEN = os.getenv("bs_api_token")
FN_TOKEN = os.getenv("fn_token")
UNB_TOKEN = os.getenv("unbelivaboat_api_token")
openai.api_key = os.getenv("openai_key")
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
        await self.tree.sync()
        await self.tree.sync(guild=guild_id1)
applicationid = 1102573935658283038
intents = discord.Intents.all()
client = MyClient(intents=intents)
guild_id = 1130945537181499542
guild_id1 = discord.Object(id=guild_id)
DiscordWebSocket.identify = identify
logs_channel = 1131864743502696588

# autres clients API
unbclient = unb.UnbeliClient(token=str(UNB_TOKEN))
blclient = bl.BlaguesAPI(token=str(BLAGUES_TOKEN))
enkaclient = enk.EnkaNetworkAPI(lang="fr", cache=True)
fnapi = ftn.FortniteAPI(api_key=str(FN_TOKEN), run_async=True)
r34py = rule34Py()

##commands
#ping
@client.tree.command(name="cash", description="[FUN] indique combien d'argent en cash possède l'utilisateur", guild=guild_id1)
async def unbcash(interaction: discord.Interaction, user: Optional[discord.Member]):
    if user == None:
        user_balance = await unbclient.get_user_balance(guild_id=guild_id, user_id=interaction.user.id)
        await interaction.response.send_message(f"voici ton cash : {user_balance.cash} <:LBmcbaguette:1140270591828570112>", ephemeral=True)
    if not user == None:
        user_balance = await unbclient.get_user_balance(guild_id=guild_id, user_id=user.id)
        await interaction.response.send_message(f"voici le cash de {user.display_name} : {user_balance.cash} <:LBmcbaguette:1140270591828570112>", ephemeral=True)
        await unbclient.close_session()

@client.tree.command(name="bank", description="[FUN] indique combien d'argent en banque possède l'utilisateur", guild=guild_id1)
async def unbbank(interaction: discord.Interaction, user: Optional[discord.Member]):
    if user == None:
        user_balance = await unbclient.get_user_balance(guild_id=guild_id, user_id=interaction.user.id)
        await interaction.response.send_message(f"voici ton cash : {user_balance.bank} <:LBmcbaguette:1140270591828570112>", ephemeral=True)
    else:
        user_balance = await unbclient.get_user_balance(guild_id=guild_id, user_id=user.id)
        await interaction.response.send_message(f"voici le cash de {user.display_name} : {user_balance.bank} <:LBmcbaguette:1140270591828570112>", ephemeral=True)
        await unbclient.close_session()
        
@client.tree.command(name="ping", description="[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb=discord.Embed(description=f"Pong ! 🏓 {round(client.latency, 1)}", color=discord.Color.blurple(),timestamp=datetime.datetime.now())
    await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="bot_info", description="permet d'obtenir les infos du bot")
async def botinfo(interaction: discord.Interaction):
    emb = discord.Embed(title=f"{client.user.display_name}'s infos", description=f"nom : {client.user.name}\n", color=discord.Color.blue(), timestamp=datetime.datetime.now())
    emb.set_footer(text=client.user, icon_url=client.user.avatar)
    emb.add_field(name="Imports", value=f"Discord.py : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}\nEnkanetwork.py :{enk.__version__}\nBlaguesAPI : ?\nFortnite API : {ftn.__version__}\nPython : {sys.version}", inline=False)
    await interaction.response.send_message(embed=emb, ephemeral=True)


#staff app system
@client.tree.command(name="staff_app", description="[MODERATION] postuler dans la modération, grâce à cette commande, c'est facile.", guild=guild_id1)
async def staff_app(interaction: discord.Interaction, file: Optional[discord.Attachment]):
    e = file
    await interaction.response.send_modal(staff(e))

class staff(discord.ui.Modal):
    def __init__(self, e):
        self.e = e
        super().__init__(title="Candidature")
        
    role = discord.ui.TextInput(label='rôle', style=discord.TextStyle.paragraph, max_length=200, placeholder="décrit nous quel rôle tu souhaite avoir", required = True)
    reason = discord.ui.TextInput(label='raison', style=discord.TextStyle.paragraph, max_length=2000, placeholder="hésitez pas avec les détails, vous avez de la place", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"ta candidature a bien été enregistrée {interaction.user.mention} !", ephemeral=True)
        emb=discord.Embed(title="Candidature", description=f"{interaction.user.display_name} vient de postuler :", color = discord.Colour.blurple(), timestamp=datetime.datetime.now())
        emb.add_field(name="Rôle sujet au recrutement :",value=self.role, inline=False)
        emb.add_field(name="Raison",value=self.reason, inline=False)
        emb.set_thumbnail(url=f"{interaction.user.avatar}")        
        emb.set_footer(text=client.user, icon_url=client.user.avatar) #Perso je fous les infos du bot la dessus
#send embed to mod chat
        staff = client.get_channel(1130945538406240399)
        staffmsg = await staff.send(embed=emb, file=self.e)

        emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
        for i in range(len(emojilist)):
            await staffmsg.add_reaction(emojilist[i])

#sendrule
@client.tree.command(name="sendrule", description = "[MODERATION]permet d'envoyer l'embed du règlement.", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.default_permissions(manage_guild=True)
async def sendrule(interaction: discord.Interaction):
    channel=client.get_channel(1130945537907114137)
    emb=discord.Embed(title="Règlement de la Boulangerie", description="# __I__. Respecter les règles de la plate-forme !\nAvant de respecter le règlement du serveur, nous vous invitons également à respecter les règles de discord :\n- [Conditions d'utilisation de Discord](https://discord.com/terms)\n- [Charte d’utilisation de la communauté Discord](https://discord.com/guidelines)\n# __II__. Langue sur le serveur :\nLe serveur et ses discussions sont uniquement en Français.\n# __III__. Soyez respectueux et ayez du bon sens !\nAyez une bonne impression au sein de la communauté ! Tous types de contenus violents, racistes et NSFW sont interdits sur ce serveur. Respectez vous peu importe vos affinités lorsque vous parlez avec le reste de la communauté. Nous ne pouvons pas tout énumérer mais n'essayez pas de contourner les règles d'une quelconque manière.\n# __IV__. Les Interdictions :\nLa publicité de n'importe quel projet sur le serveur comme dans les messages privés des autres membres est interdite. Le spam, le flood ou tout spam de mentions inutiles voir abusives vous sera sanctionné. Les comportements toxiques (troll, insultes, etc...) ainsi que les provocations n'ont rien à faire sur ce serveur. La divulgation d'informations sans consentement vous sera sanctionné.\n# __V__. Le Staff :\nL'équipe de modération vous remercierai d'avoir un pseudonyme sans caractère spéciaux ainsi qu'un profil correct et approprié. Ces règles ne sont pas négligeables et obligatoires. L'équipe de modération ainsi que l'administration aura toujours le dernier mot. En cas d'abus de l'un de nos modérateurs, merci de nous prévenir !", color = discord.Color.blue())
    emb.set_author(name="Wishrito", url="https://discordapp.com/users/911467405115535411", icon_url=f"{interaction.user.avatar}") # type: ignore
    emb.set_thumbnail(url="https://cdn.discordapp.com/icons/1115588576340606978/a_d2b27f21b84bc1b5c000b05d408a76ef.gif?size=96")        
    #send embed to rules chat
    await channel.send(embed=emb) #type: ignore
    await interaction.response.send_message("envoyé!", ephemeral=True)

#rps
@client.tree.command(name="rps", description="[FUN] Shi-Fu-Mi")
@app_commands.choices(choix=[
    app_commands.Choice(name="Pierre", value="rock"),
    app_commands.Choice(name="Papier", value="paper"),
    app_commands.Choice(name="Ciseaux", value="scissors"),
    ])
async def rps(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    rpslist = ["rock", "paper", "scissors"]
    e = random.choice(rpslist)
    e = e.replace("rock","Pierre ✊").replace("paper","Papier 🤚").replace("scissors","Ciseaux :v:")
    content = f"tu as fait {choix.name.replace('Pierre', 'Pierre ✊').replace('Papier', 'papier 🤚').replace('Ciseaux', 'Ciseaux :v:')}\nJ'ai fait {e}"
    if choix.name.replace('Pierre', 'Pierre ✊').replace('Papier', 'papier 🤚').replace('Ciseaux', 'Ciseaux :v:') == e:
        await interaction.response.send_message(content=f"{content}\n\négalité!")
    if choix.value == "scissors" and e == "Papier 🤚":
        await interaction.response.send_message(content=f"{content}\n\ntu as gagné!")
    if choix.value == "rock" and e == "Papier 🤚":
        await interaction.response.send_message(content=f"{content}\n\nj'ai gagné!")
    if choix.value == "paper" and e == "Pierre ✊":
        await interaction.response.send_message(content=f"{content}\n\ntu as gagné!")
    if choix.value == "scissors" and e == "Pierre ✊":
        await interaction.response.send_message(content=f"{content}\n\nj'ai gagné!")
    if choix.value == "rock" and e == "Ciseaux :v:":
        await interaction.response.send_message(content=f"{content}\n\ntu as gagné!")
    if choix.value == "paper" and e == "Ciseaux :v:":
        await interaction.response.send_message(content=f"{content}\n\nj'ai gagné!")

@client.tree.context_menu(name="Profil")
@app_commands.rename(user="Membre")
async def profil(interaction: discord.Interaction, user: discord.Member):
    # Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace("UserFlags.","").replace("[<","").replace(">]","").replace("hypesquad_bravery: 64","<:bravery:1137854128131932290>").replace("hypesquad_balance: 256","<:balance:1137854125120421918>").replace("hypesquad_brilliance: 128","<:brilliance:1137854120930332682>").replace("active_developer: 4194304","<:activedeveloper:1137860552257970276>").replace(">, <"," ")
    # Output
    emb = discord.Embed(title=f"Profil de {user.display_name}", color=user.color, timestamp=datetime.datetime.now())   #Tu peux meme foutre ca en bas, ca precise a quel heure a ete fait l'embed
    emb.add_field(name="Date de création du compte :", value=f"le {discord.utils.format_dt(user.created_at)}")
    emb.add_field(name="Badges :", value=badges_class)
    emb.set_thumbnail(url= f"{user.display_avatar}")   #Pour ajouter la pp du type
    emb.set_footer(text=client.user, icon_url=client.user.avatar)  #Perso je fous les infos du bot la dessus
    await interaction.response.send_message(embed=emb, ephemeral=True, view=SimpleView(url=user.avatar.url, user=user)) #type: ignore


class SimpleView(discord.ui.View):
    def __init__(self, user, url):
        super().__init__()

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label=f'photo de profil de {user.display_name}', url=url))

#sanctions system

@client.tree.command(name="ban", description = "[MODERATION][BETA] bannit un utilisateur spécifié", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à ban")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du ban")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
    channel = await client.fetch_channel(1130945537907114139)
    raison = await moderation.banfunct(interaction, member, str(reason))
    emb = discord.Embed(title="Ban", description=f"{member.mention} [{member.id}] a été banni(e).\n Auteur du banissement :{interaction.user.mention} [{interaction.user.id}]\nRaison : {reason}")
    await channel.send(embed=emb)

#sanctions system
@client.tree.command(name ="mute", description = "[MODERATION] mute un utilisateur spécifié", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à mute")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du mute")
@app_commands.rename(duration="temps")
@app_commands.describe(duration="Le temps en minutes que l'utilisateur doit être mute")
@app_commands.default_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: Optional[str] = None):
    channel = await client.fetch_channel(1131864743502696588)
    raison = await moderation.mutefunct(interaction, member, duration, str(reason))
    emb = discord.Embed(title="Mute", description=f"{member.mention} [{member.id}] a été mute.\n Auteur du mute :{interaction.user.mention} [{interaction.user.id}]\nRaison : {raison}")
    await channel.send(embed=emb)


@client.tree.command(name="kick", description="[MODERATION] kick un utilisateur spécifié", guild=guild_id1)
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à kick")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du kick")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
    channel = await client.fetch_channel(1131864743502696588)
    raison = await moderation.kickfunct(interaction, member, str(reason))
    emb = discord.Embed(title="Mute", description=f"{member.mention} [{member.id}] a été kick.\n Auteur du kick :{interaction.user.mention} [{interaction.user.id}]\nRaison : {raison}")
    await channel.send(embed=emb)

async def text_autocomplete(interaction: discord.Interaction, current: str):
    randresponse = ["tg", "qu'est-ce qu'il y a ?", "https://cdn.discordapp.com/attachments/1117749066269474866/1159221700513255504/belt_time.mp4"]
    return [
        app_commands.Choice(name=i, value=i)
        for i in randresponse
    ]

@client.tree.command(name="summon", description="permet d'invoquer un utilisateur")
@app_commands.autocomplete(phrase=text_autocomplete)
@app_commands.describe(phrase="le texte que tu veux que l'invocation dise", user="l'utilisateur que tu veux invoquer")
async def summon(interaction: discord.Interaction, user: discord.Member, phrase: Optional[str] = None):
    pdp = await user.avatar.read()
    troll = await interaction.channel.create_webhook(name=user.display_name, avatar=pdp)
    
    await interaction.response.send_message(f"{user.display_name} a été summon avec succès", ephemeral=True)

    if user.id == 340535506758795264:
        await troll.send("https://media.discordapp.net/attachments/631844119307616266/1069688737610608730/InShot_20230130_191141745.gif")
        await asyncio.sleep(2)
        await troll.delete()

    if not phrase:
        randresponse = ["tg", "qu'est-ce qu'il y a ?", "https://cdn.discordapp.com/attachments/1117749066269474866/1159221700513255504/belt_time.mp4"]
        await troll.send(random.choice(randresponse))
        await asyncio.sleep(2)
        await troll.delete()

    else:
        await troll.send(phrase)
        await asyncio.sleep(2)
        await troll.delete()

@client.tree.command(name="webhook", description="envoie un message via un webhook")
@app_commands.default_permissions(manage_guild=True)
@app_commands.describe(texte=f"ce que tu veux que le webhook dise")
@app_commands.describe(nom="le nom du webhook")
@app_commands.describe(channel="le chat dans lequel ca s'enverra")
@app_commands.describe(file="la photo de profil du webhook")
async def webhhooktroll(interaction: discord.Interaction, texte: str, nom: str, channel: Optional[discord.TextChannel], file: Optional[discord.Attachment]):
    if channel == None:
        print(file)
        if file == None:
            webhookcreate = await interaction.channel.create_webhook(name=nom, avatar=None,reason="tkt")
            await webhookcreate.send(texte)
            await interaction.response.send_message(content=f"webhook envoyé dans {interaction.channel}", ephemeral=True)
            await asyncio.sleep(2)
            await webhookcreate.send(texte)
            edit = await interaction.original_response()
            await edit.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()
            await edit.delete()
        if not file == None:
            pdp = await file.read()
            webhookcreate = await interaction.channel.create_webhook(name=nom, avatar=pdp,reason="tkt")
            await interaction.response.send_message(content=f"webhook en cours d'envoi dans {interaction.channel}...", ephemeral=True)
            await asyncio.sleep(2)
            await webhookcreate.send(texte)
            edit = await interaction.original_response()
            await edit.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()
            await edit.delete()
    if not channel == None:
        print(file)
        if file == None:
            webhookcreate = await interaction.channel.create_webhook(name=nom, avatar=None,reason="tkt")
            await interaction.response.send_message(content=f"webhook en cours d'envoi dans {interaction.channel}...", ephemeral=True)
            await asyncio.sleep(2)
            await webhookcreate.send(texte)
            editable = await interaction.original_response()
            await editable.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()
        if not file == None:
            pdp = await file.read()
            webhookcreate = await channel.create_webhook(name=nom, avatar=pdp,reason="tkt")
            await interaction.response.send_message(content=f"webhook en cours d'envoi dans {channel}...", ephemeral=True)
            await asyncio.sleep(2)
            await webhookcreate.send(texte)
            editable = await interaction.original_response()
            await editable.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()

@client.tree.command(name="blague_random", description="test")
async def randjoke(interaction: discord.Interaction):
    blague = await blclient.random()
    emb = discord.Embed(title="Blague Random 🎲", description=f"{blague.joke}\n\n||{blague.answer}||")
    await interaction.response.send_message(embed=emb, ephemeral=True)

async def blague_autocomplete(interaction: discord.Interaction, current: str):
    randresponse = ['GLOBAL', 'DEV', 'DARK', 'LIMIT', 'BEAUF', 'BLONDES']

    return [
        app_commands.Choice(name=i, value=i)
        for i in randresponse
    ]

@client.tree.command(name="blague", description="envoie une blague d'un type spécifié")
@app_commands.autocomplete(choix=blague_autocomplete)
async def joke(interaction: discord.Interaction, choix: str):
    blague = await blclient.random_categorized(choix.casefold())
    emb = discord.Embed(title=f"Blague Random {choix}", description=f"{blague.joke}\n\n||{blague.answer}||")
    await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="sync", description="[MODERATION] permet de synchroniser le tree")
@app_commands.default_permissions(manage_guild=True)
async def sync(interaction: discord.Interaction):
    await client.tree.sync(guild=guild_id1)
    await client.tree.sync()
    await interaction.response.send_message("le tree a été correctement synchronisé !", ephemeral=True)
    await asyncio.sleep(2)
    await interaction.delete_original_response()

@client.tree.command(name="fortnite_profil", description="obtenir des infos sur un compte Fortnite")
@app_commands.choices(support=[
    app_commands.Choice(name="Manette", value="controller"),
    app_commands.Choice(name="Clavier-souris", value="keyboard"),
    app_commands.Choice(name="Tactile", value="touch"),
    app_commands.Choice(name="Tous", value="all"),
    ])
@app_commands.describe(support="support de jeu recherché")
@app_commands.describe(pseudo="le pseudo de l'utilisateur")
async def fninfo(interaction: discord.Interaction, pseudo: str, support: app_commands.Choice[str]):
    try:
        e = await fnapi.stats.fetch_by_name(name=pseudo) # type: ignore
    except errors.NotFound as NotFound:
        # Créer un objet ToastNotifier
        toaster = ToastNotifier()

        # Afficher une notification
        toaster.show_toast("Bread Chan : Erreur", f"{NotFound}")
        emb = discord.Embed(title=f"Erreur", description=NotFound, color=discord.Color.orange())
        emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
        await interaction.response.send_message(embed=emb, ephemeral=True) # type: ignore
    except errors.Forbidden as Forbidden:
        # Créer un objet ToastNotifier
        toaster = ToastNotifier()

        # Afficher une notification
        toaster.show_toast("Bread Chan : Erreur", f"{Forbidden}")
        emb = discord.Embed(title=f"Erreur", description=Forbidden, color=discord.Color.orange())
        emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
        await interaction.response.send_message(embed=emb, ephemeral=True) # type: ignore
    else:
        emb = discord.Embed(title=f"Profil Fortnite de {e.user.name}", color=discord.Color.blue())
        emb.set_thumbnail(url=f"{interaction.user.avatar}") #type: ignore
        emb.set_author(name=e.user.name, icon_url=e.image_url)
        emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
        if support.value == "all":
            emb.add_field(name="Nombre de kills", value=f"Solo: {e.stats.all.solo.kills} kills <:FortniteCrosshair:1169734856884887632>\nDuo: {e.stats.all.duo.kills} kills <:FortniteCrosshair:1169734856884887632>\nSquad: {e.stats.all.squad.kills} kills <:FortniteCrosshair:1169734856884887632>") # type: ignore
        if support.value == "controller":
            emb.add_field(name="Nombre de kills", value=f"Solo: {e.stats.gamepad.solo.kills} kills <:FortniteCrosshair:1169734856884887632>\nDuo: {e.stats.gamepad.duo.kills} kills\nSquad: {e.stats.gamepad.squad.kills} kills <:FortniteCrosshair:1169734856884887632>") # type: ignore
        if support.value == "keyboard":
            emb.add_field(name="Nombre de kills", value=f"Solo: {e.stats.keyboard_mouse.solo.kills} kills <:FortniteCrosshair:1169734856884887632>\nDuo: {e.stats.keyboard_mouse.duo.kills} kills <:FortniteCrosshair:1169734856884887632>\nSquad: {e.stats.keyboard_mouse.squad.kills} kills <:FortniteCrosshair:1169734856884887632>") # type: ignore
        if support.value == "touch":
            emb.add_field(name="Nombre de kills", value=f"Solo: {e.stats.touch.solo.kills} kills <:FortniteCrosshair:1169734856884887632>\nDuo: {e.stats.touch.duo.kills} kills <:FortniteCrosshair:1169734856884887632>\nSquad: {e.stats.touch.squad.kills} kills <:FortniteCrosshair:1169734856884887632>")
        
        await interaction.response.send_message(embed=emb, ephemeral=True) # type: ignore

@client.tree.command(name="brawlstars_profil", description="obtenir des infos sur un compte Brawl Stars")
@app_commands.describe(tag="l'identifiant de l'utilisateur")
async def bsinfo(interaction: discord.Interaction, tag: str):

    bs_token = os.getenv("bs_api_token")
    bsclient = brst.Client(token=bs_token, is_async=True)

    bstag = tag.upper().replace("#", "")
    player = bsclient.get_player(bstag)
    club = player.get_club()

    hexcolorlist = ["0xffa2e3fe","0xffffffff","0xff4ddba2","0xffff9727","0xfff9775d","0xfff05637","0xfff9c908","0xffffce89","0xffa8e132","0xff1ba5f5","0xffff8afb","0xffcb5aff"]
    namecolorlist = [discord.Color.blue(), discord.Color.light_embed(), discord.Color.dark_green(), discord.Color.orange(), discord.Color.red(), discord.Color.dark_red(), discord.Color.yellow(), discord.Color.default(), discord.Color.green(), discord.Color.dark_blue(), discord.Color.pink(), discord.Color.purple()]

    i = 0

    while not player.name_color == hexcolorlist[i]:
        i = i + 1
    
    playcolor = namecolorlist[i]
    a = await other_functions.brawlerlist()    
    if club == None:  # Player n'a pas de club?

        playeremb = discord.Embed(title=f"**Profil de {player.name}**", description=f"**Tag:** {player.tag}\n\n<:bstrophy:1141793310055350353> **Trophées:** ``{player.trophies}``\n<:bstrophy:1141793310055350353> **Record Personel:** {player.highest_trophies}\n\n<:club:1169755350925320213> **Club:** Aucun\n\n**Victoires en Showdown:**\n<:showdown:1169755353748099102> {player.solo_victories} <:duo_showdown:1169755356155625543> {player.duo_victories}\n\n**Victoires en 3v3:** \n<:3v3:1169756786404901015> {player.x3vs3_victories}\n\n **Brawlers:** {len(player.brawlers)}/{a}", color=playcolor)
    else:
        playeremb = discord.Embed(title=f"**Profil de {player.name}**", description=f"**Tag:** {player.tag}\n\n<:bstrophy:1141793310055350353> **Trophées:** {player.trophies}\n<:bstrophy:1141793310055350353> **Record Personel:** {player.highest_trophies}\n\n<:club:1169755350925320213> **Club:** {club.name} ({club.tag})\n\n**Victoires en Showdown:**\n<:showdown:1169755353748099102> {player.solo_victories} <:duo_showdown:1169755356155625543> {player.duo_victories}\n\n**Victoires en 3v3:** \n<:3v3:1169756786404901015> {player.x3vs3_victories}\n\n **Brawlers:** {len(player.brawlers)}/{a}", color=playcolor)
    
    
    icon_class = str(player.icon).replace("{'id': ","https://cdn-old.brawlify.com/profile/").replace("}",".png")

    playeremb.set_thumbnail(url=icon_class)
    playeremb.set_image(url=f"https://share.brawlify.com/player/{tag}")

    await interaction.response.send_message(embed=playeremb)
    await bsclient.close()

@client.tree.command(name="genshin_profil", description="obtenir des infos sur un compte Genshin Impact")
@app_commands.describe(uid="le pseudo ou identifiant de l'utilisateur")
async def genshininfo(interaction: discord.Interaction, uid: str):
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
            await interaction.response.send_message(embed=emb, ephemeral=True, view=DropdownView(data))

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

@client.tree.command(name="r34", description="cherche une video ou image sur Rule34", nsfw=True)
@app_commands.choices(choix=[
    app_commands.Choice(name="Image", value="image"),
    app_commands.Choice(name="Vidéo", value="video")
])
@app_commands.describe(choix="le type de media")
async def r34(interaction: discord.Interaction, choix: app_commands.Choice[str], tag1: str, tag2: Optional[str], tag3: Optional[str], tag4: Optional[str], tag5: Optional[str]):
    #original list
    taglist = [choix.value, tag1, tag2, tag3, tag4, tag5]

    #sublist created with list comprehension
    #define new sublist that doesn't contain None
    taglist_updated = [value for value in taglist if value != None]


    cul = r34py.random_post(tags=taglist_updated)
    try:
        r34py.random_post(tags=taglist_updated)
    except TypeError as e:
        await interaction.response.send_message(content=e, ephemeral=True)
    else:
        base_url = "https://rule34.xxx/index.php?page=post&s=view&id="
        if 'video' in str(taglist):
            await interaction.response.send_message(content=f"``{str(taglist_updated).replace('[', '').replace(']', '')}``\n\n{cul.video}", ephemeral=True, view=r34view(base_url + str(cul.id), tags=taglist_updated))
        else:        
            await interaction.response.send_message(content=f"``{str(taglist_updated).replace('[', '').replace(']', '')}``\n\n{cul.image}", ephemeral=True, view=r34view(base_url + str(cul.id), tags=taglist_updated))

class r34view(discord.ui.View):
    def __init__(self, url: str, tags: list[str]):
        self.tags = tags
        super().__init__(timeout=None)
        self.add_item(ui.Button(label="Source", style=ButtonStyle.url, url=url))


    @ui.button(label="une autre", style=discord.ButtonStyle.blurple, emoji="🔄")
    async def on_click2(self, interaction: discord.Interaction, button: discord.ui.Button):
        base_url = "https://rule34.xxx/index.php?page=post&s=view&id="

        cul = r34py.random_post(tags=self.tags)
        try:
            r34py.random_post(tags=self.tags)
        except TypeError as e:
            await interaction.response.send_message(content=e, ephemeral=True)
        except discord.errors.NotFound as e:
            await interaction.response.send_message(content=e, ephemeral=True)
        else:
            if 'video' in str(self.tags):
                await interaction.edit_original_response(content=f"``{str(self.tags).replace('[', '').replace(']', '')}``\n\n{cul.video}", view=r34view(base_url + str(cul.id), tags=self.tags))
            else:        
                await interaction.edit_original_response(content=f"``{str(self.tags).replace('[', '').replace(']', '')}``\n\n{cul.image}", view=r34view(base_url + str(cul.id), tags=self.tags))

#report system
#def modal
class ReportModal(discord.ui.Modal, title="signalement"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(label="raison du report",min_length=1, placeholder=f"pourquoi veux-tu le signaler ?")

    async def on_submit(self, interaction: discord.Interaction):
        textinput = self.textinput
        chat = await client.fetch_channel(1130945538406240405)
        emb=discord.Embed(title="signalement", description=f"{interaction.user.display_name} vient de créer un signalement :\n\nMembre signalé : {self.msg.author.display_name}\n\nRaison : {textinput}\n\nPreuve : ``{self.msg.content}\n\n\n{self.msg.jump_url}", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"https://discordapp.com/users/{client.user.id}", icon_url=client.user.avatar)
        emb.set_image(url=self.msg.attachment[0].url)
        emb.set_thumbnail(url=f"{interaction.user.avatar}") # type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore
        #send embed to mod chat
        await chat.send(embed=emb) # type: ignore
        await interaction.response.send_message(content=f"ton signalement a bien été envoyé {interaction.user.display_name}", ephemeral=True)

@client.tree.context_menu(name="Report", guild=guild_id1)
async def report(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(ReportModal(msg))

class say(ui.Modal, title="contenu du reply"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = ui.TextInput(style=discord.TextStyle.paragraph, label="Texte", min_length=1)
    ping = ui.TextInput(style=discord.TextStyle.short, label="Mention", min_length=3, max_length=3, placeholder="Oui ou Non", required=False)
    ping2 = bool(ping.value.casefold().replace("oui", "True").replace("non", "False"))
    async def on_submit(self, interaction: discord.Interaction):
        if not self.ping:
            await self.msg.reply(self.textinput.value, mention_author=True)
            await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)
        else:
            await self.msg.reply(self.textinput.value, mention_author=self.ping2)
            await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)

class UnbanModal(discord.ui.Modal, title="Formulaire de débanissement"):
    def __init__(self):
        super().__init__()
    textinput = discord.ui.TextInput(label="Pourquoi devrait-tu être unban ?", min_length=100, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        textinput = self.textinput
        chat = await client.fetch_channel(1130945538406240405)
        emb=discord.Embed(title="Débanissement", description=f"{interaction.user.display_name} vient de créer une demande d'unban :\n\nRaison : {textinput}", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"https://discordapp.com/users/{client.user.id}", icon_url=client.user.avatar)
        emb.set_thumbnail(url=f"{interaction.user.avatar}") # type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore
        #send embed to mod chat
        await chat.send(embed=emb) # type: ignore
        await interaction.response.send_message(content=f"ta demande a bien été envoyée, {interaction.user.display_name}", ephemeral=True)

class unbanreqview(discord.ui.View):
    def __init__(self):
        super().__init__()

    guild = client.get_guild(1130945537181499542)
    unbanchat = client.get_channel(1130945538406240399)
    @discord.ui.button(label="Oui", style=discord.ButtonStyle.green)
    async def on_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        unbanchat = client.get_channel(1130945538406240399)
        guild = client.get_guild(1130945537181499542)
        emb = discord.Embed(title="Demande d'unban", description=f"{interaction.user.name, f' ({interaction.user.id})'} a envoyé une demande d'unban", timestamp=datetime.datetime.now(), color=discord.Color.green())
        emb.set_author(name=f"{guild.name}", url=guild.icon)
        emb.set_thumbnail(url=interaction.user.avatar)
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        msg = await unbanchat.send(embed=emb)
        reactlist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
        for i in range(len(reactlist)):
            await msg.add_reaction(reactlist[i])
        self.clear_items()
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Non", style=discord.ButtonStyle.red)
    async def on_click2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ok")
        self.clear_items()
        await interaction.message.edit(view=self)

last_command_time = None
@client.tree.command(name="unban_request")
async def ban_appeal(interaction: discord.Interaction):
        guild = client.get_guild(1130945537181499542)
        global last_command_time
        # Vérifiez si last_command_time est défini et si assez de temps s'est écoulé (une semaine ici)
        if last_command_time is None or (datetime.datetime.now() - last_command_time) > datetime.timedelta(hours=2):
                try:
                    await guild.fetch_ban(discord.Object(interaction.user.id))
                except discord.errors.NotFound:
                    await interaction.response.send_message("tu n'es pas banni de La Boulangerie débilus")
                else:
                    e = await guild.fetch_ban(discord.Object(interaction.user.id))                
            # Exécutez la commande
                    await interaction.response.send_message(f"Tu as été banni pour cette raison : ``{e.reason}``\n\nSouhaite-tu envoyer une demande de débanissement au staff ?", view=unbanreqview(), ephemeral=True)
            # Mettez à jour last_command_time avec la date actuelle
                last_command_time = datetime.datetime.now()
        else:
            # Informez l'utilisateur qu'il doit attendre
            await interaction.response.send_message(f"Tu dois encore attendre {datetime.datetime.now() - last_command_time} avant de pouvoir utiliser cette commande.", ephemeral=True)

@client.tree.context_menu(name="Say")
@app_commands.default_permissions(manage_guild=True)
async def pins(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(say(msg))
    await interaction.channel.typing()

# async def colorautocomplete(interaction: discord.Interaction, current: str):
#     colorlist = ["0x3498DB"]
#     
#     return [
#         app_commands.Choice(name=i, value=i)
#         for i in colorlist
#     ]
# @client.tree.command(name="role_edit", description="[PREMIUM] permet de modifier votre role unique", guild=guild_id1)
# @app_commands.autocomplete(role=colorautocomplete)
# @app_commands.choices(option=[
#     app_commands.Choice(name="Modifier", value="edit"),
#     app_commands.Choice(name="Créer", value="create"),
#     ])
# async def rolecolorchange(interaction: discord.Interaction, option: app_commands.Choice[str], role: Optional[str]):
#     await roledumec.edit(color=discord.Color.from_str(str(role)))

#auto events

##module d'edition de messages
@client.event
async def on_message_edit(before, after):
    if before.author.bot == True or before.author == client.user or before.content == after.content:
        return
    else:
        if before.guild.id == 1130945537181499542:
            emb = discord.Embed(description=f"**{after.author.display_name}** a édité son message:", timestamp=datetime.datetime.now())
            emb.set_author(name="Message modifié", icon_url="https://cdn.discordapp.com/attachments/1139849206308278364/1142035263590236261/DiscordEdited.png")
            emb.add_field(name="avant", value=f"{before.content}\n\n{after.jump_url}", inline=True)
            emb.add_field(name="après", value=f"{after.content}", inline=True)
            emb.set_thumbnail(url=after.author.display_avatar)
            emb.set_footer(text=client.user, icon_url=client.user.avatar)
            webfetch = await client.fetch_channel(1131864743502696588)
            await webfetch.send(embed=emb)

        if before.guild.id == 1130798906586959946:
            emb = discord.Embed(description=f"**{after.author.display_name}** a édité son message:", timestamp=datetime.datetime.now())
            emb.set_author(name="Message modifié",icon_url="https://cdn.discordapp.com/attachments/1139849206308278364/1142035263590236261/DiscordEdited.png")
            emb.add_field(name="avant", value=f"{before.content}\n\n{after.jump_url}", inline=True)
            emb.add_field(name="après", value=f"{after.content}", inline=True)
            emb.set_thumbnail(url=after.author.display_avatar)
            emb.set_footer(text=client.user, icon_url=client.user.avatar)
            webfetch = await client.fetch_channel(1141995718228324482)
            await webfetch.send(embed=emb)
        else:
            return

#module des logs de supression de messages
@client.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    else:
        if message.guild.id == 1130945537181499542: # La Boulangerie
            channel = await client.fetch_channel(1131864743502696588)
            if message.attachments:
                e = []
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n```{message.content}```", color=discord.Color.brand_red(), type="image")
                emb.add_field(name="chat:", value=message.channel.jump_url)
                for _ in message.attachments:
                    e.append(emb.add_field(name=_.filename, value=_.url, inline=False))
                await channel.send(embed=emb)
            else:
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n```{message.content}```", color=discord.Color.brand_red())
                emb.add_field(name="chat:", value=message.channel.jump_url)
                await channel.send(embed=emb)

        if message.guild.id == 1130798906586959946: # BreadStudios Lab
            channel1 = await client.fetch_channel(1141995718228324482)
            liste = []
            if message.attachments:
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n```{message.content}```", color=discord.Color.brand_red(), type="image")
                emb.add_field(name="chat:", value=message.channel.jump_url)
                for _ in message.attachments:
                    liste.append(emb.add_field(name=f"{_.filename}", value=_.url, inline=False))
                await channel1.send(embed=emb)
            else:
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n```{message.content}```", color=discord.Color.brand_red())
                emb.add_field(name="chat:", value=message.channel.jump_url)
                await channel1.send(embed=emb)
        else:
            return

## module de message de bienvenue
@client.event
async def on_member_join(member: discord.Member):
    LBchannel = client.get_channel(1130945537907114139)
    Kchannel = client.get_channel(1129912901847765002)
    statchannel = client.get_channel(1163733415229669376)
    if member.guild == LBchannel.guild:
        # Ouvrir l'image
        await member.avatar.save(f"src/buffer/{member.id}.png")
        image = Image.open(f"src/buffer/{member.id}.png")

        # Créer un masque circulaire transparent en mode "L" (Luminance)
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        width, height = image.size
        circle_radius = min(width, height) // 2
        circle_center = (width // 2, height // 2)
        draw.ellipse((circle_center[0] - circle_radius, circle_center[1] - circle_radius, circle_center[0] + circle_radius, circle_center[1] + circle_radius), fill=255)

        # Convertir le masque en image "RGBA" avec un canal alpha
        mask = mask.convert("L")
        mask_data = mask.getdata()
        mask.putdata([pixel for pixel in mask_data])

        # Appliquer le masque transparent à l'image
        image.putalpha(mask)

        # Enregistrez l'image avec le masque circulaire transparent
        image.save(f"src/buffer/{member.id}.png")

        # Charger l'image avec le masque circulaire transparent
        image_with_transparent_circle = Image.open(f"src/buffer/{member.id}.png")

        # Charger l'image de fond
        background_image = Image.open("src/img/welcomer/synthwave.png")  # Remplacez "background.jpg" par le chemin de votre image de fond

        # Superposer l'image avec le masque circulaire transparent sur l'image de fond
        background_image.paste(image_with_transparent_circle, (0, 0), image_with_transparent_circle)

        # Convertir l'image en mode RGBA
        background_image = background_image.convert("RGBA")

        # Créer un objet ImageDraw pour ajouter du texte
        draw = ImageDraw.Draw(background_image)

        # Charger une police (assurez-vous d'avoir une police TTF installée)
        font = ImageFont.truetype("src/font/ComicSans.ttf", 28) # Remplacez le chemin et la taille

        # Obtenez le nom du membre à partir de discord.py (remplacez member_obj par l'objet de membre réel)

        member_name = f"Bienvenue sur le serveur {member.display_name} !"

        # Position pour afficher le texte (ajustez selon vos besoins)
        text_position = (60, 450)

        # Couleur du texte (en RGB)
        text_color = (255, 255, 255)

        # Ajoutez le texte à l'image
        draw.text(text_position, member_name, fill=text_color, font=font)

        # Enregistrez l'image superposée
        background_image.save("src/img/buffer/bienvenue.png")  # Vous pouvez spécifier un chemin de fichier différent si nécessaire
        file = discord.File("src/img/buffer/bienvenue.png", filename="bienvenue.png")
        
        emb=discord.Embed(title="Nouveau pain!", description=f"Un nouveau pain vient de rejoindre ! Bienvenue sur {member.guild.name} {member.display_name}! :french_bread:", color = discord.Color.pink(), timestamp=datetime.datetime.now())
        emb.set_author(name=member.guild.name, icon_url=member.guild.icon, url=f"https://discordapp.com/users/{client.user.id}")
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        emb.set_image(url="attachment://bienvenue.png")
        msg = await LBchannel.send(content=f"{member.mention}", file=file, silent=True)
        await msg.add_reaction("<:LBgigachad:1134177726585122857>")

        rolelist = [1151548927942860872, 1151549497399324732, 1151549661765709894, 1151549293749075979, 1151554619265265816, 1130945537194078317] # dans l'ordre : GNP, PINGS, LEVEL, JEUX, AUTRES, petits pains
        clearcount = len([x for x in member.guild.members if not x.bot])
        await statchannel.edit(name=f"Utilisateurs : {clearcount}")
        os.remove("src/img/buffer/bienvenue.png")
        os.remove(f"src/buffer/{member.id}.png")
        for i in range(len(rolelist)):
            await member.add_roles(discord.Object(rolelist[i]))

    if member.guild == Kchannel.guild:
        emb=discord.Embed(title="Nouveau Horny!", description=f"Un nouveau membre horny vient de rejoindre ! Bienvenue sur {member.guild.name} {member.display_name}! <:kOrgasme:1142062446421475439>", color = discord.Color.pink(), timestamp=datetime.datetime.now())
        emb.set_author(name=member.guild.name, icon_url=member.guild.icon, url=f"https://discordapp.com/users/{client.user.id}")
        emb.set_footer(text=client.user, icon_url=client.user.avatar)

        msg = await Kchannel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore
        await msg.add_reaction("<:LBgigachad:1134177726585122857>")

##module des messages d'au revoir
@client.event
async def on_member_remove(member: discord.Member):
    LBchannel = client.get_channel(1130945537907114139)
    Kchannel = client.get_channel(1129912901847765002)
    statchannel = client.get_channel(1163733415229669376)

    if member.guild == LBchannel.guild:
        clearcount = len([x for x in member.guild.members if not x.bot])
        await statchannel.edit(name=f"Utilisateurs : {clearcount}")
        emb=discord.Embed(title="Au revoir!", description=f"Notre confrère pain {member.name} vient de brûler... Nous lui faisons nos plus sincères adieux. :saluting_face:", color = discord.Color.red(), timestamp=datetime.datetime.now())
        emb.set_author(name=member.guild.name, icon_url=member.guild.icon)
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        msg = await LBchannel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore
        await msg.add_reaction("<:LBroger:1136059237441749132>")

    if member.guild == Kchannel.guild:
        emb=discord.Embed(title="Au revoir!", description=f"Notre confrère horny {member.name} vient de nous quitter... Nous lui faisons nos plus sincères adieux. :saluting_face:", color = discord.Color.red(), timestamp=datetime.datetime.now())
        emb.set_author(name=member.guild.name, icon_url=member.guild.icon, url=f"{client.user.id}")
        emb.set_footer(text=client.user, icon_url=client.user.avatar)
        msg = await Kchannel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore
        await msg.add_reaction("<:kNotFine:1131273911254925412>")
    else:
        return

@client.event
async def on_message(message: discord.Message):
    luxurechannel = await client.fetch_channel(1132379187227930664)
    LBstaffrole = luxurechannel.guild.get_role(1130945537227632648)
    e = message.content.casefold()

    if message.author.bot == True:
        return
    if message.channel.guild ==luxurechannel.guild:
        if message.channel.id == 1134102319580069898:
            await message.create_thread(name=f"QOTD de {message.author.display_name}")

        if message.channel.id == 1130945537907114141:
            await message.create_thread(name=f"Annonce de {message.author.display_name}")
            await message.publish()

        if message.channel.id == 1153333206372855818:
            await message.create_thread(name=f"Annonce de {message.author.display_name}")
            await message.add_reaction("<:LBgigachad:1134177726585122857>")

        if message.channel == luxurechannel:
            if LBstaffrole in message.author.roles:
                if message.attachments:
                    emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                    await message.create_thread(name=f"{message.author}")
                    for i in range(len(emojilist)):
                        await message.add_reaction(emojilist[i])
    
                if not message.attachments:
                    word = ["discordapp.com", "rule34.xxx", "pornhub.com"]
                    for i in range(len(word)):
                        if word[i] in str(message.content):
                            emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                            await message.create_thread(name=f"{message.author}")
                            for i in range(len(emojilist)):
                                await message.add_reaction(emojilist[i])
                else:
                    return
            else:
                if message.attachments:
                    emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                    await message.create_thread(name=f"{message.author}")
                    for i in range(len(emojilist)):
                        await message.add_reaction(emojilist[i])

                if not message.attachments:
                    word = ["discordapp.com", "rule34.xxx", "pornhub.com"]
                    for i in range(len(word)):
                        if word[i] in str(message.content):
                            emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                            await message.create_thread(name=f"{message.author}")
                            for i in range(len(emojilist)):
                                await message.add_reaction(emojilist[i])
                        else:
                            await message.delete()
                            await message.author.send(f"tu n'es pas autorisé à envoyer des messages textuels dans {message.channel.mention}", file=discord.File("src/img/Steam-access-is-denied.webp"))

# en gros, si y a un message, si le message n'a pas été envoyé par moi ou goblet, qu'il est envoyé dans la luxure, et qu'il a pas de pièce jointe, ca le delete

    if not message.author.id == 911467405115535411: # fonction qui m'immunise de ces conneries

        if " bite" in e:
            await message.channel.typing()
            await asyncio.sleep(2)
            await message.reply("https://cdn.discordapp.com/attachments/778672634387890196/1142544668488368208/nice_cock-1.mp4")

        if "UwU" in e:
            await message.add_reaction("<a:DiscoUwU:1158497203615187015>")

        word1 = "quoi"
        if e.endswith(word1): # Verifie si la combinaison est dans le message ET si x = 1
            await message.channel.typing()
            await message.reply("coubaka! UwU")

        if message.content.startswith(client.user.mention):
            await message.channel.typing()
            await asyncio.sleep(3)
            rand = random.randint(1, 2)
            if rand == 1:
                await message.reply("https://cdn.discordapp.com/attachments/928389065760464946/1131347327416795276/IMG_20210216_162154.png")
            if rand == 2:
                await message.reply(file=discord.File("src/audio/HORN.mp3"))

        if message.content.startswith("<:LBhfw1:1133660402081865788> <:LBhfw2:1133660404665548901>"):
           await message.reply("t'es pas très sympa, tu mérite [10h de ayaya](https://www.youtube.com/watch?v=UCDxZz6R1h0)!")
        randcramptes1 = "cramptés ?".casefold()
        randcramptes2 = ["https://didnt-a.sk/", "https://tenor.com/bJniJ.gif", "[ok](https://cdn.discordapp.com/attachments/1139849206308278364/1142583449530683462/videoplayback.mp4)", "[.](https://cdn.discordapp.com/attachments/1130945537907114145/1139100471907336243/Untitled_video_-_Made_with_Clipchamp.mp4)", "tg"]
        for i in range(len(randcramptes1)):    #Check pour chaque combinaison
            if e.startswith(f"t'as les {randcramptes1[i]}"):  #Verifie si la combinaison est dans le message
                await message.channel.typing()
                await message.reply(random.choice(randcramptes2))
                break
        if ":moyai:" in message.content:
            await message.reply("https://canary.discord.com/store/skus/1037148024792690708/moai")

    word2 = ["https://tiktok.com/", "https://vm.tiktok.com/", "https://www.tiktok.com/"]
    for i in range(len(word2)):    #Check pour chaque combinaison
        if word2[i] in message.content:
            vxTiktokResolver = str(message.content).replace('https://tiktok.com/', 'https://vxtiktok.com/').replace("https://vm.tiktok.com/","https://vm.vxtiktok.com/").replace("<h","h").replace("> "," ")
            await message.channel.send(content=f"résolution du Tiktok envoyé par {message.author.display_name}[:]({vxTiktokResolver})")
            await message.delete()

    if message.channel.id == 1130945537907114145 and message.attachments:
        if random.randint(1, 50) == 1:
            await message.add_reaction(random.choice(client.emojis))

#auto tasks

@tasks.loop(seconds=20)  # Temps entre l'actualisation des statuts du bot
async def changepresence():
    guild = client.get_guild(1130945537181499542)
    apple = client.get_user(1014832884764393523)
    clearcount = len([x for x in guild.members if not x.bot])
    randmember = random.choice(guild.members)
    randmember2 = random.choice(guild.members)
    game = [
            f"{apple.display_name} en train de chialer",
            "Lilo et Nightye sur Smash",
            "Amouranth, mais pas sur Twitch",
            "Amouranth dire que JDG ressemble à un ananas",
            "ce bg de Cyrger qui a payé pour mon hébergement",
            "webstrator.com",
            "pas ma mère sur Pornhub !",
            f"à quoi jouent les {clearcount} membres du serveur",
            "Chainsaw Man sur Crunchyroll",
            "un porno gay avec DraftBot et Dyno",
            "mon 69ème statut.",
            "maman, je passe à la télé !",
            f"{guild.owner.display_name}, traverse la rue et tu trouveras du travail",
            "pas Boku No Pico",
            "Wishrito se faire enculer sur Fortnite pendant que GobletMurt regarde",
            f"{guild.owner.display_name} toucher de l'herbe (c'est faux)",
            "Alan faire du bon contenu",
            "les nudes de DraftBot",
            "Fallen Condoms",
            "mec, le serveur est actif !",
            f"la bite de {randmember.display_name}. ah, nan j'ai rien dit, elle est si petite que je la vois pas!",
            "un enfant et prie pour qu'un camion passe",
            "Mee6 sous la douche~",
            "un documentaire sur Auschwitz",
            "Sword Art Online",
            "GobletMurt mettre un balais dans le cul de Milanozore",
            "Enka.Network",
            f"les {clearcount} membres du serveur !",
            "Lotharie et sa colonne dans le cul",
            "Fenrixx se faire chasser par les furries",
            f"{apple.display_name} qui regarde Alex in Harlem",
            "Maniak troller Lotharie",
            "Krypto qui est perdu",
            "les muscles saillants des staff",
            "Rule34",
            "La Breadmacht envahir la Pologne",
            "Monster Musume",
            f"l'appendice pénétrant de daddy {guild.owner.name.title()}~ UwU",
            "le OnlyFans de Nightye",
            "Chuislay en train de répendre la sainte baguette",
            "mec, je me transforme en sexbot!",
            f"le journal de {guild.name}",
            "Nightye qui a retrouvé le trophée 1m de Wankil",
            f"{randmember.display_name} réduire {randmember2.display_name} en esclavage",
        ]
    activity = discord.Activity(type = discord.ActivityType.watching, name=random.choice(game))
    await client.change_presence(activity=activity, status=discord.Status.online)

#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + " Build Infos " + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}")
    await changepresence.start()
    try:
        # Récupère l'émoji.
        # emojiID correspond à l'ID de l'émoji en question.
        emojiIDlist =[
            1136229377399603210,
            1163003539715534929,
            1138549194550952048,
            1136234211976695888,
            1136241845899374722,
            1136247065291268147,
            1136241241781186632,
            1139089457086210118,
            1136242676195406015,
            1136229172935659640,
            1136232472418455622,
            1136236032455606364,
            1136232168402735234,
            1136234618417328218,
            1136233292899819532
            ]
        
        # guildID correspond à l'ID du serveur où se trouve l'émoji.
        guild = await client.fetch_guild(guild_id)

        # Récupère le rôle.
        # roleID correspond à l'ID du rôle qui doit avoir accès à l'émoji.
        staffrole = 1130945537215053942
        botrole = 1130945537194078316
        devrole = 1130945537181499543

        # Ajoute le rôle à la liste des rôles ayant accès à l'émoji.
        for i in range(len(emojiIDlist)):
            e = discord.Object(emojiIDlist[i], type=discord.Emoji)
            await e.edit(roles=[discord.Object(staffrole), discord.Object(botrole), discord.Object(devrole)])
    except discord.errors.Forbidden and discord.errors.HTTPException as e:
        print(e)

client.run(str(DISCORD_TOKEN))