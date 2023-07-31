#imports
import discord, os, datetime, random, requests, pprint
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from typing import Optional
import sys
from discord.gateway import DiscordWebSocket, _log

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
botlink="https://discordapp.com/users/793183664858071040"
boticonurl="https://cdn.discordapp.com/avatars/1102573935658283038/872ee23bdd10cf835335bd98a5981bc2.webp?size=128"
DiscordWebSocket.identify = identify
headers = {"Authorization": f"Bot {os.getenv('discord_token')}"}
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
        channel=client.get_channel(1115615150251192420)
        emb=discord.Embed(title="Candidature", description=f"```{interaction.user.display_name} vient de postuler :\r\n rôle sujet au recrutement : {self.role}\r\n Raison : {self.reason}```", color = discord_blue, timestamp=datetime.datetime.now())
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

#send modal
@client.tree.context_menu(name="Signaler")
async def report(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_modal(test2())

#report system
class test2(discord.ui.Modal, title=f"signalement"):
    reason = discord.ui.TextInput(label='raison', style=discord.TextStyle.paragraph, max_length=200)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"ton signalement a bien été effectué {interaction.user.display_name} !", ephemeral=True)
        channel=client.get_channel(1130945538406240405)
        emb=discord.Embed(title="signalement", description=f"{interaction.user.display_name} vient de créer un signalement :\r\n Membre signalé : {discord.Member}\r\n Raison : {self.reason}\r\n Preuve : {interaction.message}```", color = red, timestamp=datetime.datetime.now())
        emb.set_author(name="BreadBot", url=f"{botlink}", icon_url=f"{boticonurl}")
        emb.set_thumbnail(url=f"{interaction.user.avatar}") # type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore            
#send embed to mod chat
        await channel.send(embed=emb) #type: ignore

@client.tree.context_menu(name="Profil", guild=guild_id1)
async def badges(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace('[<', '').replace("UserFlags.","").replace('>]', '').replace('_', ' ').replace(':', '').replace(">","").replace("<","").title()

    # Remove digits from string
    badges_class = ''.join([i for i in badges_class if not i.isdigit()])
    
    # Output
    emb = discord.Embed(title=f"Profil de {user.display_name}", description=f"Date de création du compte :\n> le {user.created_at.day}/{user.created_at.month}/{user.created_at.year} à {user.created_at.hour}h{user.created_at.minute}\nBadges :\n> {badges_class}", color=user.color)
    emb.set_thumbnail(url=user.display_avatar,)
    await interaction.response.send_message(embed=emb, ephemeral=True, view=SimpleView(url=user.avatar.url))
class SimpleView(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        
        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label='Clique ici', url=url))

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

@client.tree.command(name="test", description="test", guild=guild_id1)
@app_commands.default_permissions(manage_guild=True)
async def test(interaction: discord.Interaction):
    req = requests.get(f"https://discord.com/api/v9/users/{interaction.user.id}", headers=headers)
    await interaction.response.send_message(req.json(), ephemeral=True)
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
    emb=discord.Embed(title="Nouveau Pain!", description=f"Un nouveau pain vient de sortir du four ! Bienvenue sur {member.guild.name} {member.name}! <:Chad:1115629188049813534> :french_bread:\npour commencer, va dans https://discord.com/channels/1130945537181499542/1130945537907114140 et effectue la commande </captcha:1131468501870182436>", color = green, timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}")
    emb.set_footer(text=f"{member.name}, sur {member.guild.name}", icon_url=member.guild.icon)            
    channel = client.get_channel(1130945537907114139)
    await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
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
                await message.reply("https://didnt-a.sk/")
                break
        
#auto tasks
@tasks.loop(seconds=20)  # Temps entre l'actualisation des statuts du bot
async def changepresence():
    global x
    game = iter(
        [
            "pas ma mère sur Pornhub !",
            "à quoi jouent les membres du serveur",
            "Chainsaw Man sur Crunchyroll",
            "un porno gay avec DaftBot et Dyno",
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
    print(f"Discord info : {discord.version_info.serial}")
    await changepresence.start()
client.run(DISCORD_TOKEN)  # type: ignore