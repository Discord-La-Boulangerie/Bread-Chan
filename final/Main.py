#imports
import discord, os, datetime, random, requests, pprint, json
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from typing import Optional
import sys
from discord.gateway import DiscordWebSocket, _log
from blagues_api import BlaguesAPI, BlagueType, Blague, CountJoke, main
import brawlstats
from brawlstats import Ranking, Player, Members, Client, Club, Constants, Brawlers, BattleLog, NotFoundError, models, core
from enkanetwork import EnkaNetworkAPI, EnkaPlayerNotFound
import fortnite_api
from fortnite_api import StatsImageType, AccountType, BrBannerImage, BrPlayerStats, Playlist


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
enkaclient = EnkaNetworkAPI(lang="fr", cache=True)
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
        await self.tree.sync(guild=guild_id1)
        await self.tree.sync()
intents = discord.Intents.all()
client = MyClient(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned_or("K!"))
blue = discord.Color.from_rgb(0, 0, 200)
red = discord.Color.from_rgb(200, 0, 0)
green = discord.Color.from_rgb(0, 200, 0)
discord_blue = discord.Color.from_rgb(84, 102, 244)
guild_id = 1130945537181499542
guild_id1 = discord.Object(id=guild_id)
botlink="https://discordapp.com/users/1102573935658283038"
boticonurl="https://cdn.discordapp.com/avatars/1102573935658283038/872ee23bdd10cf835335bd98a5981bc2.webp?size=128"
DiscordWebSocket.identify = identify
# Set up the OpenAI API client

##commands
#ping
@client.tree.command(name = "ping", description = "[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb=discord.Embed( description="Pong ! 🏓 <:Chad:1115629188049813534>", color=discord_blue,timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}") # type: ignore
    emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore            
    await interaction.response.send_message(embed=emb, ephemeral=True)
#staff app system
class staff(discord.ui.Modal, title="Candidature"):
    role = discord.ui.TextInput(label='rôle', style=discord.TextStyle.paragraph, max_length=200, placeholder="décrit nous quel rôle tu souhaite avoir", required = True)
    reason = discord.ui.TextInput(label='raison', style=discord.TextStyle.paragraph, max_length=2000, placeholder="hésitez pas avec les détails, vous avez de la place", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"ta candidature a bien été enregistrée {interaction.user.mention} !", ephemeral=True)
        channel=client.get_channel(1130945538406240399)
        emb=discord.Embed(title="Candidature", description=f"```{interaction.user.display_name} vient de postuler :\n\n rôle sujet au recrutement : {self.role}\n\n Raison : {self.reason}```", color = discord_blue, timestamp=datetime.datetime.now())
        emb.set_author(name="BreadBot", url=f"{botlink}", icon_url=f"{boticonurl}") # type: ignore
        emb.set_thumbnail(url=f"{interaction.user.avatar}")        
        emb.set_footer(text=f"{interaction.user.display_name}, sur {interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore            
#send embed to mod chat
        await channel.send(embed=emb) #type: ignore

@client.tree.command(name = "staff_app", description = "[MODERATION] postuler dans la modération, grâce à cette commande, c'est facile.")
async def staff_app(interaction: discord.Interaction):
    await interaction.response.send_modal(staff())

#sendrule
@client.tree.command(name = "sendrule", description = "[MODERATION]permet d'envoyer l'embed du règlement.") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.default_permissions(manage_guild=True)
async def sendrule(interaction: discord.Interaction):
    channel=client.get_channel(1130945537907114137)
    emb=discord.Embed(title="Règlement de la Boulangerie", description="# __I__. Respecter les règles de la plate-forme !\nAvant de respecter le règlement du serveur, nous vous invitons également à respecter les règles de discord :\n- [Conditions d'utilisation de Discord](https://discord.com/terms)\n- [Charte d’utilisation de la communauté Discord](https://discord.com/guidelines)\n# __II__. Langue sur le serveur :\nLe serveur et ses discussions sont uniquement en Français.\n# __III__. Soyez respectueux et ayez du bon sens !\nAyez une bonne impression au sein de la communauté ! Tous types de contenus violents, racistes et NSFW sont interdits sur ce serveur. Respectez vous peu importe vos affinités lorsque vous parlez avec le reste de la communauté. Nous ne pouvons pas tout énumérer mais n'essayez pas de contourner les règles d'une quelconque manière.\n# __IV__. Les Interdictions :\nLa publicité de n'importe quel projet sur le serveur comme dans les messages privés des autres membres est interdite. Le spam, le flood ou tout spam de mentions inutiles voir abusives vous sera sanctionné. Les comportements toxiques (troll, insultes, etc...) ainsi que les provocations n'ont rien à faire sur ce serveur. La divulgation d'informations sans consentement vous sera sanctionné.\n# __V__. Le Staff :\nL'équipe de modération vous remercierai d'avoir un pseudonyme sans caractère spéciaux ainsi qu'un profil correct et approprié. Ces règles ne sont pas négligeables et obligatoires. L'équipe de modération ainsi que l'administration aura toujours le dernier mot. En cas d'abus de l'un de nos modérateurs, merci de nous prévenir !", color = discord_blue)
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
async def profil(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace("UserFlags.","").replace("[<","").replace(">]","").replace("hypesquad_bravery: 64","<:bravery:1137854128131932290>").replace("hypesquad_balance: 256","<:balance:1137854125120421918>").replace("hypesquad_brilliance: 128","<:brilliance:1137854120930332682>").replace("active_developer: 4194304","<:activedeveloper:1137860552257970276>").replace(">, <"," ")

    # Output
    emb = discord.Embed(title=f"Profil de {user.display_name}", description=f"Date de création du compte :\n> le {user.created_at.day}/{user.created_at.month}/{user.created_at.year} à {user.created_at.hour}h{user.created_at.minute}\nBadges :\n{badges_class}", color=user.color)
    emb.set_thumbnail(url=user.display_avatar)
    await interaction.response.send_message(embed=emb, ephemeral=True, view=SimpleView(url=user.avatar.url, user=user)) #type: ignore
class SimpleView(discord.ui.View):
    def __init__(self, user, url):
        super().__init__()
        
        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label=f'photo de profil de {user.display_name}', url=url))

        return
#sanctions system
@client.tree.command(name ="ban", description = "[MODERATION][BETA] bannit un utilisateur spécifié") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à ban")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du ban")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason:Optional[str] = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été ban pour la raison suivante :\n{reason}", ephemeral=True)
    channel = await client.fetch_channel(1130945537907114139)
    await channel.send(content=f"{member.mention} a été ban du serveur par {interaction.user.name}") # type: ignore

@client.tree.command(name="kick", description="[MODERATION] kick un utilisateur spécifié")
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à kick")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du kick")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason:Optional[str] = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été kick pour la raison suivante :\n{reason}", ephemeral=True)
    channel = await client.fetch_channel(1130945537907114139)
    await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore

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
    except EnkaPlayerNotFound as vr:
        emb=discord.Embed(title="Erreur", url="https://enka.network/404", description=f"=== UID introuvable ===\n\n{vr}", color = red, timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=f"{boticonurl}")
        emb.set_thumbnail(url=f"{interaction.user.display_icon}") #type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) #type: ignore
        await interaction.response.send_message(embed=emb, ephemeral=True)
    else:
        emb=discord.Embed(title=f":link: Vitrine Enka de {data.player.nickname}", url=f"https://enka.network/u/{uid}", description=f"=== Infos du compte ===\n\nRang d'aventure: {data.player.level} | Niveau du monde: {data.player.world_level}\n\nBio: {data.player.signature}\n\n<:achievements:1129447087667433483> Succès: {data.player.achievement}\n\n<:abyss:1129447202566180905> Profondeurs spiralées : étage {data.player.abyss_floor} | salle {data.player.abyss_room}", color = blue, timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=f"{boticonurl}")
        emb.set_thumbnail(url=f"{data.player.avatar.icon.url}")
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) #type: ignore
        await interaction.response.send_message(embed=emb, ephemeral=True, view=DropdownView(data))

class Dropdown(discord.ui.Select):
    def __init__(self, data):
        self.data = data
        # Set the options that will be presented inside the dropdown
        options=[]
        for char in self.data.characters:
            options.append(discord.SelectOption(label=f"{char.name}", description=f"le build de {char.name}", value=char.id)) # add dropdown option for each character in data.character
            super().__init__(placeholder="Sélectionne le build que tu souhaite regarder :", min_values=1, max_values=1, options=options)

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
    async def callback(self, interaction: discord.Interaction):

        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
            emb=discord.Embed(title=f"{self.data.player.nickname}'s {self.values[0]}", description=f"Voici les informations du personnage:\n\n{self}", color = green, timestamp=datetime.datetime.now())
            emb.set_author(name=f"{client.user}", icon_url=f"{self.data.player.avatar.icon.url}", url=f"https://enka.network/u/{self.data.uid}")
            emb.set_footer(text=f"{interaction.user.name}", icon_url=interaction.guild.icon) #type: ignore     
            await interaction.response.send_message(f"Voici le build de {self.values[0]}:", ephemeral=True, embed=emb)

class DropdownView(discord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data=data
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(data))
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
        emb=discord.Embed(title="signalement", description=f"{interaction.user.display_name} vient de créer un signalement :\n\nMembre signalé : {self.msg.author.display_name}\n\nRaison : {textinput}\n\nPreuve : {self.msg.content}\n\n\n [aller au message]({self.msg.jump_url})", color = red, timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=f"{boticonurl}")
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

#auto events
@client.event
async def on_member_remove(member: discord.Member):
    channel=client.get_channel(1130945537907114139)
    emb=discord.Embed(title="Au revoir!", description=f"Notre confrère pain {member.name} vient de brûler... Nous lui faisons nos plus sincères adieux. :saluting_face:", color = red, timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}")
    emb.set_footer(text=f"{member.name}, sur {member.guild.name}", icon_url=member.guild.icon)       
    await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore

@client.event 
async def on_member_join(member: discord.Member):
    emb=discord.Embed(title="Nouveau Pain!", description=f"Un nouveau pain vient de sortir du four ! Bienvenue sur {member.guild.name} {member.display_name}! :french_bread:", color = green, timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}")
    emb.set_footer(text=f"{member.name}, sur {member.guild.name}", icon_url=member.guild.icon)            
    channel = client.get_channel(1130945537907114139)
    await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.channel.id == 1134102319580069898:
        qotd = await message.create_thread(name=f"QOTD de {message.author.display_name}")
        await qotd.send(f"Thread créé automatiquement pour la QOTD de {message.author.mention}")
    
    if message.channel.id == 1130945537907114141:
        announcements = await message.create_thread(name=f"Annonce de {message.author.display_name}")
        botmsg = await announcements.send(f"Thread créé automatiquement pour l'annonce de {message.author.mention}")
        await message.publish()
        await botmsg.pin()
    if not message.author.id == 911467405115535411:
        if message.channel.id == 1132379187227930664:
            if not message.attachments:
                word = ["https://cdn.discordapp.com", "https://rule34.xxx", "https://fr.pornhub.com/"]
                for i in range(len(word)):
                    if word[i] in message.content:
                        return
                    else:    
                        await message.delete()
                        await message.author.send(f"tu n'as pas la permission d'envoyer des messages textuels dans {message.channel.mention} 🙄") #type: ignore
# en gros, si y a un message, si le message n'a pas été envoyé par moi, qu'il est envoyé dans la luxure, et qu'il a pas de pièce jointe, ca le delete

    if not message.author.id == 911467405115535411:
        word1 = ["quoi", "QUOI", "Quoi", "quoi ?", "QUOI ?", "Quoi ?", "quoi?", "QUOI?", "Quoi?"]
        for i in range(len(word1)):    #Check pour chaque combinaison
            if message.content.endswith(word1[i]):  #Verifie si la combinaison est dans le message ET si x = 1
                await message.reply("coubaka! UwU")
                break
        if message.content.startswith("<@1102573935658283038>"):
            await message.reply("https://cdn.discordapp.com/attachments/928389065760464946/1131347327416795276/IMG_20210216_162154.png")
        if message.content.startswith("<:HFW1:1133660402081865788> <:HFW2:1133660404665548901>"):
           await message.reply("t'es pas très sympa, tu mérite [10h de ayaya](https://www.youtube.com/watch?v=UCDxZz6R1h0)!")
        word2 = ["cramptés","cramptes","cramptés ?", "cramptés?"]
        for i in range(len(word2)):    #Check pour chaque combinaison
            if message.content.startswith(f"t'as les {word2[i]}"):  #Verifie si la combinaison est dans le message
                rand = ["https://didnt-a.sk/", "https://tenor.com/bJniJ.gif", "[ok](https://cdn.discordapp.com/attachments/1120352052871176292/1135884018185928754/Oh_no_cringe_but_in_french.mp4)",]
                await message.reply(rand[random.randint(1, 3)])
                break
    word2 = ["https://tiktok.com/", "https://vm.tiktok.com/", "https://www.tiktok.com/"]
    for i in range(len(word2)):    #Check pour chaque combinaison
        if word2[i] in message.content:
            vxTiktokResolver = str(message.content).replace('https://tiktok.com/', 'https://vxtiktok.com/').replace("https://vm.tiktok.com/","https://vm.vxtiktok.com/").replace("<h","h").replace("> ","")
            await message.reply(content=f"[résolution du lien :]({vxTiktokResolver})", mention_author=False)

#auto tasks
@tasks.loop(seconds=20)  # Temps entre l'actualisation des statuts du bot
async def changepresence():
    global x
    game = iter(
        [
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
    )   #liste des statuts du bot ^
    for x in range(random.randint(1, 37)):  # le nombre total de statuts différents
        x = next(game)
    activity = discord.Activity(type = discord.ActivityType.watching, name=f"{x}")
    await client.change_presence(activity=activity, status=discord.Status.online)


#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + " Build Infos " + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
    await changepresence.start()
client.run(DISCORD_TOKEN)  # type: ignore