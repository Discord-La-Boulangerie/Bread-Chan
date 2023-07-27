#imports
import discord, os, datetime, random
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
        await self.tree.sync()
intents = discord.Intents.all()
client = MyClient(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned_or("K!"))
blue = discord.Color.from_rgb(0, 0, 200)
red = discord.Color.from_rgb(200, 0, 0)
green = discord.Color.from_rgb(0, 200, 0)
discord_blue = discord.Color.from_rgb(84, 102, 244)
DiscordWebSocket.identify = identify

##commands
#ping
@client.tree.command(name = "ping", description = "[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    botlink = f"https://discordapp.com/users/{client.user.id}"
    boticonurl = client.user.display_avatar.url
    emb=discord.Embed( description="Pong ! 🏓", color=discord_blue,timestamp=datetime.datetime.now())
    emb.set_author(name=client.user.display_name, icon_url=f"{boticonurl}", url=f"{botlink}") # type: ignore
    emb.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon) # type: ignore            
    await interaction.response.send_message(embed=emb, ephemeral=True)

#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + " Build Infos " + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
client.run(DISCORD_TOKEN)  # type: ignore