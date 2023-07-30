#imports
import discord, os, datetime, random, sys, json
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from typing import Optional
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

@client.tree.context_menu(name="profil", guild=guild_id)
async def badges(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace('[<', '').replace("UserFlags.","").replace('>]', '').replace('_', ' ').replace(':', '').replace(">","").replace("<","").title()

    # Remove digits from string
    badges_class = ''.join([i for i in badges_class if not i.isdigit()])
    activ = user.activity
    # Output
    emb = discord.Embed(title=f"Profil de {user.display_name}", description=f"Date de création du compte :\n> le {user.created_at.date()} à {user.created_at.hour}h{user.created_at.minute}\nBadges :\n> {badges_class}\nActivité :\n> {activ}", color=user.color)
    emb.set_thumbnail(url=user.display_avatar)
    await interaction.response.send_message(embed=emb, ephemeral=True)

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

#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + "| Build Infos |" + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
client.run(DISCORD_TOKEN)  # type: ignore