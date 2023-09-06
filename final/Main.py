#Import des libs python de base
import os, sys
import datetime
import json
import random
from dotenv import load_dotenv
from typing import Optional
from io import BytesIO
import asyncio
from collections import Counter


#Import de discord et modules discord
import discord 
from discord import app_commands
from discord.ext import tasks
from discord.gateway import DiscordWebSocket, _log
from discord.utils import MISSING

#Import des API
import unbelipy as unb
import blagues_api as bl
import brawlstats as brst
import enkanetwork as enk
from enkanetwork.model.stats import Stats
import fortnite_api as ftn

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

load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")
BLAGUES_TOKEN = os.getenv("blagues_api_token")
BS_TOKEN = os.getenv("bs_api_token")
FN_TOKEN = os.getenv("fn_token")
UNB_TOKEN = os.getenv("unbelivaboat_api_token")
enkaclient = enk.EnkaNetworkAPI(lang="fr", cache=True)
# client def
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
botlink=f"https://discordapp.com/users/1102573935658283038"
DiscordWebSocket.identify = identify
logs_channel = 1131864743502696588

unbclient = unb.UnbeliClient(token=str(UNB_TOKEN))
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
    if not user == None:
        user_balance = await unbclient.get_user_balance(guild_id=guild_id, user_id=user.id)
        await interaction.response.send_message(f"voici le cash de {user.display_name} : {user_balance.bank} <:LBmcbaguette:1140270591828570112>", ephemeral=True)
        await unbclient.close_session()

@client.tree.command(name="leaderboard", description="[FUN] indique le classement global du serveur", guild=guild_id1)
async def leaderboard(interaction: discord.Interaction):
    guild_leaderboard = await unbclient.get_guild_leaderboard(guild_id)
    await interaction.response.send_message(content="test", view=verifyview(interaction), ephemeral=True)

class verifyview(discord.ui.View):
    def __init__(self, interaction):
        self.interaction = interaction
        super().__init__()

    @discord.ui.button(label="précédent", style=discord.ButtonStyle.green)
    async def on_click1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.interaction.edit_original_response(content="test1")
    
    @discord.ui.button(label="suivant", style=discord.ButtonStyle.red)
    async def on_click2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.interaction.edit_original_response(content="test2")

@client.tree.command(name="ping", description="[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb=discord.Embed(description=f"Pong ! 🏓 {round(client.latency, 1)}", color=discord.Color.blurple(),timestamp=datetime.datetime.now())

    await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.command(name="bot_info", description="permet d'obtenir les infos du bot", guild=guild_id1)
async def botinfo(interaction: discord.Interaction):
    emb = discord.Embed(title=f"{client.user.display_name}'s infos", description=f"nom : {client.user.name}\n", color=discord.Color.blue(), timestamp=datetime.datetime.now())
    emb.set_footer(text=client.user, icon_url=client.user.avatar) #Perso je fous les infos du bot la dessus
    emb.add_field(name="Imports", value=f"Discord.py : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}\nEnkanetwork.py :{enk.__version__}\nBlaguesAPI \nFortnite API : {ftn.__version__}\nPython : {sys.version}", inline=False)
    await interaction.response.send_message(embed=emb, ephemeral=True)


#staff app system
@client.tree.command(name = "staff_app", description = "[MODERATION] postuler dans la modération, grâce à cette commande, c'est facile.", guild=guild_id1)
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
@client.tree.command(name = "sendrule", description = "[MODERATION]permet d'envoyer l'embed du règlement.", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
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
@client.tree.command(name="rps", description="[FUN][BETA] Shi-Fu-Mi")
@app_commands.choices(choix=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ])
async def rps(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    if (choix.value == 'rock'):
        await interaction.response.send_message("paper! :scroll:", ephemeral=True) 
    elif (choix.value == 'paper'):
        await interaction.response.send_message("scissors! :scissors:", ephemeral=True)
    else:
        await interaction.response.send_message("rock! :rock:", ephemeral=True)

@client.tree.context_menu(name="Profil", guild=guild_id1)
@app_commands.rename(user="Membre")
async def profil(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace("UserFlags.","").replace("[<","").replace(">]","").replace("hypesquad_bravery: 64","<:bravery:1137854128131932290>").replace("hypesquad_balance: 256","<:balance:1137854125120421918>").replace("hypesquad_brilliance: 128","<:brilliance:1137854120930332682>").replace("active_developer: 4194304","<:activedeveloper:1137860552257970276>").replace(">, <"," ")

    # Output

#NEW
    emb = discord.Embed(
    title=f"Profil de {user.display_name}",
    color=user.color,
    timestamp= datetime.datetime.now()   #Tu peux meme foutre ca en bas, ca precise a quel heure a ete fait l'embed
    )
    emb.add_field(name="Date de création du compte :", value=f"le {user.created_at.day}/{user.created_at.month}/{user.created_at.year} à {user.created_at.hour}h{user.created_at.minute}")
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
@client.tree.command(name ="ban", description = "[MODERATION][BETA] bannit un utilisateur spécifié", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à ban")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du ban")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason:Optional[str] = None):
    if not interaction.user.id == interaction.guild.owner_id : #type: ignore
        if interaction.user.top_role <= member.top_role: #type: ignore
            await interaction.response.send_message(f"tu n'as pas la permission de ban {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", ephemeral=True, color=discord.Color.red()) #type: ignore
        else:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été ban pour la raison suivante :\n{reason}", ephemeral=True)
            channel = await client.fetch_channel(1130945537907114139)
            await channel.send(content=f"{member.mention} a été ban du serveur par {interaction.user.name}") #type: ignore
    else:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été ban pour la raison suivante :\n{reason}", ephemeral=True)
        channel = await client.fetch_channel(1130945537907114139)
        await channel.send(content=f"{member.mention} a été ban du serveur par {interaction.user.name}") #type: ignore

#sanctions system
@client.tree.command(name ="mute", description = "[MODERATION] mute un utilisateur spécifié", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à mute")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du mute")
@app_commands.rename(duration="temps")
@app_commands.describe(duration="Le temps que l'utilisateur doit être mute")
@app_commands.describe(file="le fichier contenant la preuve de la raison")
@app_commands.rename(file="fichier")
@app_commands.default_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason:Optional[str], file: Optional[discord.Attachment]):
    channel = await client.fetch_channel(1131864743502696588)
    if not interaction.user.id == member.id:  
        if interaction.user.top_role.position <= member.top_role.position: #type: ignore
            emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", color=discord.Color.dark_embed(), timestamp=datetime.datetime.now())
            await interaction.response.send_message(embed=emb, ephemeral=True) #type: ignore
        else:
            if reason == None:
                await member.timeout(datetime.timedelta(seconds=float(duration)), reason="a surement fait quelque chose qui n'est pas acceptable")
                await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute {duration} minutes", ephemeral=True)
                emb = discord.Embed(title="Sanction",description=f"{member.mention} a été mute par {interaction.user.mention}", timestamp=datetime.datetime.now(), color=discord.Color.red())
                emb.set_field_at(index=1, name="preuve de la raison du mute", value=file)
                await channel.send(embed=emb) #type: ignore
            else:
                await member.timeout(datetime.timedelta(seconds=float(duration)), reason="a surement fait quelque chose qui n'est pas acceptable")
                await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute {duration} minutes pour la raison suivante : {reason}", ephemeral=True)
                emb = discord.Embed(title="Sanction",description=f"{member.mention} a été mute par {interaction.user.mention}", timestamp=datetime.datetime.now(), color=discord.Color.red())
                emb.set_field_at(index=1, name="preuve de la raison du mute", value=file)
                await channel.send(embed=emb) #type: ignore
    
    if interaction.user.id == member.id:
        await interaction.response.send_message("wtf t'as vraiment pas d'amour propre pour essayer de te mute toi-même ou ca se passe comment ?", ephemeral=True)
    else :
        if interaction.user.id == interaction.guild.owner_id : #type: ignore:
            await member.timeout(datetime.timedelta(seconds=float(duration)))
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute pour la raison suivante :\n{reason}", ephemeral=True)
            emb = discord.Embed(title="Sanction", description=f"{member.mention} a été mute par {interaction.user.mention}", timestamp=datetime.datetime.now(), color=discord.Color.red())
            emb.set_image(url=file)
            await channel.send(embed=emb) #type: ignore

@client.tree.command(name="kick", description="[MODERATION] kick un utilisateur spécifié", guild=guild_id1)
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à kick")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du kick")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str], file: Optional[discord.Attachment] = None):
    if not interaction.user.id == interaction.guild.owner_id : #type: ignore
        if interaction.user.top_role <= member.top_role: #type: ignore
            emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", color=discord.Color.red()) #type: ignore
            await interaction.response.send_message(embed=emb, ephemeral=True)
        else:
            if reason == None:
                await member.kick(reason="n'a pas respecté les règles")
                await interaction.response.send_message(f"{member.display_name} (id = {member.id}) a bien été kick", ephemeral=True)
                channel = await client.fetch_channel(1130945537907114139)
                await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore
            else:
                await member.kick(reason=reason)
                await interaction.response.send_message(f"{member.display_name} (id = {member.id}) a bien été kick", ephemeral=True)
                channel = await client.fetch_channel(1130945537907114139)
                await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore
    else:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.display_name} (id = {member.id}) a bien été kick pour la raison suivante :\n{reason}", ephemeral=True)
        channel = await client.fetch_channel(1130945537907114139)
        await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore

@client.tree.command(name="webhook", description="envoie un message via un webhook", guild=guild_id1)
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
            edit = await interaction.original_response()
            await edit.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()
            await edit.delete()
        if not file == None:
            pdp = await file.read()
            webhookcreate = await channel.create_webhook(name=nom, avatar=pdp,reason="tkt")
            await interaction.response.send_message(content=f"webhook en cours d'envoi dans {channel}...", ephemeral=True)
            await asyncio.sleep(2)
            await webhookcreate.send(texte)
            edit = await interaction.original_response()
            await edit.edit(content="webhook envoyé!") 
            await asyncio.sleep(5)
            await webhookcreate.delete()
            await edit.delete()

@client.tree.command(name="sync", description="[MODERATION] permet de synchroniser le tree")
@app_commands.default_permissions(manage_guild=True)
async def sync(interaction: discord.Interaction):
    await client.tree.sync(guild=guild_id1)
    await client.tree.sync()
    await interaction.response.send_message("le tree a été correctement synchronisé !", ephemeral=True)

@client.tree.command(name="game_info", description="[BETA] permet d'obtenir des infos sur un compte de jeu", guild=guild_id1)
@app_commands.choices(choix=[
    app_commands.Choice(name="Genshin", value="gi"),
    app_commands.Choice(name="Fortnite", value="fn"),
    app_commands.Choice(name="Brawl Stars", value="bs"),
    ])
@app_commands.describe(choix="Choisissez le jeu (pour le moment seul Genshin Impact fonctionne, à moitié)")
@app_commands.describe(uid="le pseudo ou identifiant de l'utilisateur")
async def gameinfo(interaction: discord.Interaction, choix: app_commands.Choice[str], uid: str):
        if choix.value == "bs":
            await interaction.response.send_message("cette fonction n'a pas encore été implémentée", ephemeral=True)
        if choix.value == "fn":
            await interaction.response.send_message("cette fonction n'a pas encore été implémentée", ephemeral=True)
        if choix.value == "gi":
            data = await enkaclient.fetch_user(uid)
        try: 
            data = await enkaclient.fetch_user(uid)
        except enk.VaildateUIDError as vr:
            emb=discord.Embed(title="Erreur", url="https://enka.network/404", description=f"=== UID introuvable ===\n\n{vr}", color = discord.Colour.red(), timestamp=datetime.datetime.now())
            emb.set_thumbnail(url=f"{interaction.user.display_icon}") #type: ignore
            emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
            await interaction.response.send_message(embed=emb, ephemeral=True)
        else:
            emb=discord.Embed(title=f":link: Vitrine Enka de {data.player.nickname}", url=f"https://enka.network/u/{uid}", description=f"=== Infos du compte ===\n\nRang d'aventure: {data.player.level} | Niveau du monde: {data.player.world_level}\n\nBio: {data.player.signature}\n\n<:achievements:1129447087667433483> Succès: {data.player.achievement}\n\n<:abyss:1129447202566180905> Profondeurs spiralées : étage {data.player.abyss_floor} | salle {data.player.abyss_room}", color = discord.Color.blue(), timestamp=datetime.datetime.now())
            emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=client.user.avatar)
            emb.set_thumbnail(url=f"{data.player.avatar.icon.url}")
            emb.set_footer(text=f"{client.user}", icon_url=client.user.avatar)
            await interaction.response.send_message(embed=emb, ephemeral=True, view=DropdownView(data))
class Dropdown(discord.ui.Select):
    def __init__(self, data):
        self.data = data
        # Set the options that will be presented inside the dropdown
        options=[]
        for char in self.data.characters:
            self.char= char
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
        emb=discord.Embed(title=f"{self.data.player.nickname}'s {self.values[0].title()}", description=f"Voici les informations du personnage:\n\ncrit rate: {NotImplemented}", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", icon_url=f"{self.data.player.avatar.icon.url}", url=f"https://enka.network/u/{self.data.uid}")
        emb.set_footer(text=f"{interaction.user.name}", icon_url=interaction.guild.icon) #type: ignore     
        await interaction.response.send_message(f"Voici le build de {self.values[0].title()}:", ephemeral=True, embed=emb)

class DropdownView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=float(10))
        self.data = data
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(data))

        async def on_timeout():
            self.clear_items
#report system

#def modal
class ReportModal(discord.ui.Modal, title="signalement"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(label="raison du report",min_length=1, placeholder=f"pourquoi veux-tu le signaler ?")
    
    async def on_submit(self, interaction: discord.Interaction):
        textinput = self.textinput
        chat = await client.fetch_channel(int(1130945538406240405))
        emb=discord.Embed(title="signalement", description=f"{interaction.user.display_name} vient de créer un signalement :\n\nMembre signalé : {self.msg.author.display_name}\n\nRaison : {textinput}\n\nPreuve : {self.msg.content}\n\n\n [aller au message]({self.msg.jump_url})", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=client.user.avatar)
        emb.set_thumbnail(url=f"{interaction.user.avatar}") # type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore
        #send embed to mod chat
        await chat.send(embed=emb) # type: ignore
        await interaction.response.send_message(content=f"ton signalement a bien été envoyé {interaction.user.display_name}", ephemeral=True)

@client.tree.context_menu(name="Report", guild=guild_id1)
async def report(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(ReportModal(msg))

class say(discord.ui.Modal, title="contenu du reply"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(label="texte",min_length=1)

    async def on_submit(self, interaction: discord.Interaction):

        await self.msg.reply(self.textinput.value)
        await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)

@client.tree.context_menu(name="Say", guild=guild_id1)
@app_commands.default_permissions(manage_guild=True)
async def pins(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(say(msg))
    await interaction.channel.typing()
#auto events

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    if before.author.bot == True:
        return
    if before.content == after.content:
        return
    else:
        if before.guild.id ==1130945537181499542:
            emb = discord.Embed(description=f"**{after.author.display_name}** a édité son message:", timestamp=datetime.datetime.now())
            emb.set_author(name="Message modifié",icon_url="https://cdn.discordapp.com/attachments/1139849206308278364/1142035263590236261/DiscordEdited.png")
            emb.add_field(name="avant", value=before.content, inline=True)
            emb.add_field(name="après", value=f"{after.content}\n\n{after.jump_url}", inline=True)
            emb.set_thumbnail(url=after.author.display_avatar)
            emb.set_footer(text=client.user, icon_url=client.user.avatar)
            webfetch = await client.fetch_channel(1131864743502696588)
            await webfetch.send(embed=emb)
        if before.guild.id ==1130798906586959946:
            emb = discord.Embed(description=f"**{after.author.display_name}** a édité son message:", timestamp=datetime.datetime.now())
            emb.set_author(name="Message modifié",icon_url="https://cdn.discordapp.com/attachments/1139849206308278364/1142035263590236261/DiscordEdited.png")
            emb.add_field(name="avant", value=before.content, inline=True)
            emb.add_field(name="après", value=f"{after.content}\n\n{after.jump_url}", inline=True)
            emb.set_thumbnail(url=after.author.display_avatar)
            emb.set_footer(text=client.user, icon_url=client.user.avatar)
            webfetch = await client.fetch_channel(1141995718228324482)
            await webfetch.send(embed=emb)
        else:
            return

@client.event
async def on_message_delete(message: discord.Message):
    if message.author == client.user:
        return
    if message.author.bot == True:
        return
    else:
        if message.guild.id == 1130945537181499542: # La Boulangerie
            channel = await client.fetch_channel(1131864743502696588)
            if message.attachments:
                e = []
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n{message.content}", color=discord.Color.brand_red(), type="image")
                emb.add_field(name="chat:", value=message.channel.jump_url)
                for i in message.attachments:
                    e.append(emb.add_field(name=i.filename, value=i.url, inline=False))
                await channel.send(embed=emb)
            else:
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n{message.content}", color=discord.Color.brand_red())
                emb.add_field(name="chat:", value=message.channel.jump_url)
                await channel.send(embed=emb)

        if message.guild.id ==1130798906586959946: # BreadStudios Lab
            channel = await client.fetch_channel(1141995718228324482)
            if message.attachments:
                e = []
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n{message.content}", color=discord.Color.brand_red(), type="image")
                emb.add_field(name="chat:", value=message.channel.jump_url)
                for i in message.attachments:
                    e.append(emb.add_field(name=f"{i.filename}", value=i.url, inline=False))
                await channel.send(embed=emb)
            else:
                emb=discord.Embed(title=f"un message de {message.author.name} a été supprimé", description=f"contenu du message : \n{message.content}", color=discord.Color.brand_red())
                emb.add_field(name="chat:", value=message.channel.jump_url)
                await channel.send(embed=emb)
#auto events
@client.event
async def on_member_remove(member: discord.Member):
    channel=client.get_channel(1130945537907114139)
    emb=discord.Embed(title="Au revoir!", description=f"Notre confrère pain {member.name} vient de brûler... Nous lui faisons nos plus sincères adieux. :saluting_face:", color = discord.Color.red(), timestamp=datetime.datetime.now())
    emb.set_author(name=member.guild.name, icon_url=member.guild.icon, url=f"{botlink}")
    emb.set_footer(text=client.user, icon_url=client.user.avatar)       
    msg = await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore
    await msg.add_reaction("<:LBroger:1136059237441749132>")
@client.event 
async def on_member_join(member: discord.Member):
    emb=discord.Embed(title="Nouveau Pain!", description=f"Un nouveau pain vient de sortir du four! Bienvenue sur {member.guild.name} {member.display_name}! :french_bread:", color = discord.Color.green(), timestamp=datetime.datetime.now())
    emb.set_author(name=member.guild.name, icon_url=member.guild.icon, url=f"{botlink}")
    emb.set_footer(text=client.user, icon_url=client.user.avatar)
    emb.add_field(name="", value="")
    channel = client.get_channel(1130945537907114139)
    msg = await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore
    await msg.add_reaction("<:LBgigachad:1134177726585122857>")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot == True:
        return
    if message.channel.id == 1134102319580069898:
        qotd = await message.create_thread(name=f"QOTD de {message.author.display_name}")
        await qotd.send(f"Thread créé automatiquement pour la QOTD de {message.author.name}")
    
    if message.channel.id == 1130945537907114141:
        announcements = await message.create_thread(name=f"Annonce de {message.author.display_name}")
        botmsg = await announcements.send(f"Thread créé automatiquement pour l'annonce de {message.author.name}")
        await message.publish()
        await botmsg.pin()
    if message.channel.id == 1132379187227930664:
        if message.author.id == 601041630081974292:
            if message.attachments:
                emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                for i in range(len(emojilist)):
                    await message.add_reaction(emojilist[i])
            if not message.attachments:
                word = ["https://cdn.discordapp.com", "https://rule34.xxx", "https://pornhub.com/"]
                for i in range(len(word)):
                    if word[i] in str(message.content):
                        emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                        for i in range(len(emojilist)):
                            await message.add_reaction(emojilist[i])
                            break
            else:
                return
        if message.author.id == 911467405115535411:
            if message.attachments:
                emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                for i in range(len(emojilist)):
                    await message.add_reaction(emojilist[i])
            else:
                word = ["https://cdn.discordapp.com", "https://rule34.xxx", "https://pornhub.com/"]
                for i in range(len(word)):
                    if word[i] in str(message.content):
                        emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                        for i in range(len(emojilist)):
                            await message.add_reaction(emojilist[i])
                            break
        else:
            if not message.attachments:
                word = ["https://cdn.discordapp.com", "https://rule34.xxx", "https://pornhub.com/"]
                for i in range(len(word)):
                    if word[i] in str(message.content):
                        emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                        for i in range(len(emojilist)):
                            await message.add_reaction(emojilist[i])
                            break
                    else:
                        try:
                            await message.delete()
                        except discord.errors.NotFound as err:
                            print(err)
                        else:
                            await message.author.send(f"tu n'est pas autorisé à envoyer des messages textuels dans {message.channel.mention}", file=discord.File("src/img/Steam-access-is-denied.webp"))
                            return
            else:
                emojilist = ["<:Upvote:1141354962392199319>","<:Downvote:1141354959372304384>"]
                for i in range(len(emojilist)):
                    await message.add_reaction(emojilist[i])
# en gros, si y a un message, si le message n'a pas été envoyé par moi ou goblet, qu'il est envoyé dans la luxure, et qu'il a pas de pièce jointe, ca le delete
    if not message.author.id == 911467405115535411:
        if "bite" in message.content:
            await message.channel.typing()
            await asyncio.sleep(2)
            await message.reply("https://cdn.discordapp.com/attachments/778672634387890196/1142544668488368208/nice_cock-1.mp4")
        word1 = ["quoi", "quoi ?", "quoi?"]
        for i in range(len(word1)):    #Check pour chaque combinaison
            e = word1[i].casefold()
            if message.content.endswith(e):  #Verifie si la combinaison est dans le message ET si x = 1
                await message.channel.typing()
                await message.reply("coubaka! UwU")
                break
        if message.content.startswith(client.user.mention):
            await message.channel.typing()
            await asyncio.sleep(3)
            await message.reply("https://cdn.discordapp.com/attachments/928389065760464946/1131347327416795276/IMG_20210216_162154.png")
        if message.content.startswith("<:LBhfw1:1133660402081865788> <:LBhfw2:1133660404665548901>"):
           await message.reply("t'es pas très sympa, tu mérite [10h de ayaya](https://www.youtube.com/watch?v=UCDxZz6R1h0)!")
        randcramptes1 = ["cramptés","cramptes","cramptés ?", "cramptés?"]
        for i in range(len(randcramptes1)):    #Check pour chaque combinaison
            randcramptes2 = ["https://didnt-a.sk/", "https://tenor.com/bJniJ.gif", "[ok](https://cdn.discordapp.com/attachments/1139849206308278364/1142583449530683462/videoplayback.mp4)", "[.](https://cdn.discordapp.com/attachments/1130945537907114145/1139100471907336243/Untitled_video_-_Made_with_Clipchamp.mp4)"]
            if message.content.startswith(f"t'as les {randcramptes1[i]}"):  #Verifie si la combinaison est dans le message
                await message.channel.typing()
                await message.reply(random.choice(randcramptes2))
                break
    word2 = ["https://tiktok.com/", "https://vm.tiktok.com/", "https://www.tiktok.com/"]
    for i in range(len(word2)):    #Check pour chaque combinaison
        if word2[i] in message.content:
            vxTiktokResolver = str(message.content).replace('https://tiktok.com/', 'https://vxtiktok.com/').replace("https://vm.tiktok.com/","https://vm.vxtiktok.com/").replace("<h","h").replace("> "," ")
            await message.channel.send(content=f"résolution du lien Tiktok envoyé à l'origine par {message.author.display_name}[:]({vxTiktokResolver})")
            await message.delete()
    if message.channel.id == 1130945537907114145:
        if random.randint(1, 50) == 1:
            if message.attachments:
                await message.add_reaction("<:LBmeh:1131556048948449400>")
        if random.randint(1, 50) == 2:
            if message.attachments:
                await message.add_reaction(":recycle:")

#auto tasks
@tasks.loop(seconds=20)  # Temps entre l'actualisation des statuts du bot
async def changepresence():
    game = [
            "pas ma mère sur Pornhub !",
            "à quoi jouent les membres du serveur",
            "Chainsaw Man sur Crunchyroll",
            "un porno gay avec DraftBot et Dyno",
            "mon 69ème statut.",
            "maman, je passe à la télé !",
            "Wishrito, traverse la rue et tu trouveras du travail",
            "pas Boku No Pico",
            "Wishrito se faire enculer sur Fortnite pendant que GobletMurt regarde",
            "Wishrito toucher de l'herbe (c'est faux)",
            "Alan faire du bon contenu",
            "les nudes de DraftBot",
            "Fallen Condoms",
            "mec, le serveur est actif !",
            "ta bite ! ah nan, elle est si petite que je la vois pas!",
            "un enfant et prie pour qu'un camion passe",
            "Mee6 sous la douche~",
            "un documentaire sur Auschwitz",
            "Sword Art Online",
            "GobletMurt mettre un balais dans le cul de Milanozore",
            "Enka.Network",
            "les membres du serveur !",
            "Lotharie et sa colonne dans le cul",
            "Fenrixx en train de chasser des furries",
            "i est apple qui regarde Alex in Harlem",
            "Maniak troller Lotharie",
            "Krypto qui est perdu",
            "les muscles saillants des staff",
            "Rule34",
            "La breadmacht envahir la Pologne",
            "Monster Musume",
            "l'appendice pénétrant de daddy Fenrixx~ UwU",
            "le OnlyFans de Nightye",
            "Chuislay en train de répendre la sainte baguette",
            "mec, je me transforme en sexbot!",
            "le journal de la Boulangerie",
            "Nightye qui a retrouvé le trophée 1m de Wankil",        
        ]
    activity = discord.Activity(type = discord.ActivityType.watching, name=f"{game[random.randint(1, len(game)-1)]}")
    await client.change_presence(activity=activity, status=discord.Status.online)

@client.event
async def on_audit_logs_entry_create(entry: discord.AuditLogEntry):
    if entry.guild.id == 1130945537181499542:
        channel = client.get_channel(1131864743502696588)
        emb= discord.Embed(title="Logs", description=f"{entry.user} ({entry.user_id}) a {entry.action}\n raison: {entry.reason}")
        await channel.send(embed=emb)



#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + " Build Infos " + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro} | {discord.version_info.releaselevel}")
    await changepresence.start()
    for i in client.guilds:
        bsemoji = await i.fetch_emoji(1138549194550952048)
    # Récupère le rôle.
    # roleID correspond à l'ID du rôle qui doit avoir accès à l'émoji.
        staffrole = discord.utils.get(i.roles, id=1130945537227632648)
        botrole = discord.utils.get(i.roles, id=1130945537194078316)
        devfrole = discord.utils.get(i.roles, id=1144410413069500548)
        myList = ["Collection", 15, (botrole, devfrole, staffrole)]
    # Ajoute le rôle à la liste des rôles ayant accès à l'émoji.
        await bsemoji.edit(roles=myList, reason="test")
client.run(str(DISCORD_TOKEN))