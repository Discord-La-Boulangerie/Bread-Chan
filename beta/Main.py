#imports
import discord, os, datetime, random, sys, json, time
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from typing import Optional
from discord.gateway import DiscordWebSocket, _log
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
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
guild_id = discord.Object(id=1130798906586959946)
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
        await self.tree.sync(guild=guild_id)
intents = discord.Intents.all()
client = MyClient(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned)
bot.owner_id=911467405115535411
blue = discord.Color.from_rgb(0, 0, 200)
red = discord.Color.from_rgb(200, 0, 0)
green = discord.Color.from_rgb(0, 200, 0)
discord_blue = discord.Color.from_rgb(84, 102, 244)
DiscordWebSocket.identify = identify
##commands
#ping
@client.tree.command(name = "ping", description = "[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    botlink = f"https://discordapp.com/users/{client.user.id}" #type: ignore
    boticonurl = client.user.display_avatar.url #type: ignore
    emb=discord.Embed( description="Pong ! 🏓", color=discord_blue,timestamp=datetime.datetime.now())
    emb.set_author(name=client.user.display_name, icon_url=f"{boticonurl}", url=f"{botlink}") # type: ignore
    emb.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon) # type: ignore            
    await interaction.response.send_message(embed=emb, ephemeral=True)

@client.tree.context_menu(name="Profil", guild=guild_id)
@app_commands.rename(user="Membre")
async def profil(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace("UserFlags.","").replace("[<","").replace(">]","").replace("hypesquad_bravery: 64","<:bravery:1137854128131932290>").replace("hypesquad_balance: 256","<:balance:1137854125120421918>").replace("hypesquad_brilliance: 128","<:brilliance:1137854120930332682>").replace("active_developer: 4194304","<:activedeveloper:1137860552257970276>").replace(">, <"," ")

    # Output

#NEW
    emb = discord.Embed(
    title=f"Profile de {user.display_name}",
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


#rps
@client.tree.command(name="sync", description="[ADMIN] permet de syncroniser le tree")
@app_commands.default_permissions(manage_guild=True)
@app_commands.choices(choix=[
    app_commands.Choice(name="Global", value="global"),
    app_commands.Choice(name="Guild", value="guild")
    ])
async def rps(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    if (choix.value == 'global'):
        await client.tree.sync()
        await interaction.response.send_message("le tree Global a bien été synchronisé", ephemeral=True) 
    elif (choix.value == 'guild'):
        await client.tree.sync(guild=guild_id)
        await interaction.response.send_message("le tree du serveur a bien été synchronisé", ephemeral=True)
@client.tree.command(name="snap", description="test", guild=guild_id)
async def snap(interaction: discord.Interaction):
    filename = f"{interaction.user.display_name}.webp"
    await interaction.user.avatar.save(filename)
    avatar = Image.open(filename).convert('RGB')
    avatar = avatar.resize((285, 285))
    bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size)
    avatar.putalpha(mask)

    output = ImageOps.fit(avatar, mask.size, centering=(1420, 298))
    output.putalpha(mask)
    output.save(f'{interaction.user.name}.webp')

    files = discord.File(fp=filename)
    await interaction.response.send_message(file=files, ephemeral=True)


@client.tree.command(name="uid_save", description="[FUN][INFO] enregistre ton UID Genshin Impact", guild=guild_id)
@app_commands.describe(amount="l'UID de ton compte Genshin Impact")
@app_commands.rename(amount="uid")
async def add_score(interaction: discord.Interaction, amount: int):
    if os.path.isfile("db.json"):
        with open("db.json", "r") as fp:
            data = json.load(fp)
        try:
            data[f"{interaction.user.name}"]["Genshin UID"] = amount
        except KeyError: # if the user isn't in the file, do the following
            data[f"{interaction.user.name}"] = {"Genshin UID": amount} # add other things you want to store
            await interaction.response.send_message(f"ton profil a été créé et ton UID a bien été enregistrée !\n> UID : {amount}", ephemeral=True)
    else:
        data = {f"{interaction.user.name}": {"Genshin UID": amount}}
    # saving the file outside of the if statements saves us having to write it twice
    with open("db.json", "w+") as fp:
        json.dump(data, fp, sort_keys=True, indent=4) # kwargs for beautification
        await interaction.response.send_message(f"ton UID a bien été modifiée!\n> UID : {amount}", ephemeral=True)
   # you can also return the new/updated score here if you want

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return
    if msg.channel.id == 1134102319580069898:
        await msg.create_thread(name="QOTD")
    
    word1 = [
        "Salut",
        "Hey",
        "salut",
        "hey",]
    for i in range(len(word1)):    #Check pour chaque combinaison
        if msg.content.startswith(f"<@{client.user.id}> {word1[i]}"): #type: ignore
            rand = [
                "entry1",
                "entry2",
                "entry3",
                ]
            await msg.reply(rand[random.randint(0, 3)])
    
    word2 = ["https://tiktok.com/", "https://vm.tiktok.com/", "https://www.tiktok.com/"]
    for i in range(len(word2)):    #Check pour chaque combinaison
        if word2[i] in msg.content:
            vxTiktokResolver = str(msg.content).replace('https://tiktok.com/', 'https://vxtiktok.com/').replace("https://vm.tiktok.com/","https://vm.vxtiktok.com/").replace("<h","h").replace("> ","")
            await msg.reply(content=f"résolution du lien :\n{vxTiktokResolver}", mention_author=False)


#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + "| Build Infos |" + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
client.run(DISCORD_TOKEN)  # type: ignore