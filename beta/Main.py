#imports
import discord, os, datetime, random, sys, json, time
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from typing import Optional
from discord.gateway import DiscordWebSocket, _log
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import aiohttp
import asyncio
from rule34Py import rule34Py

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
guild_id = 1001496918343553094
guild_id1 = discord.Object(id=guild_id)

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

intents = discord.Intents.all()
client = MyClient(intents=intents)
DiscordWebSocket.identify = identify
##commands

client.tree.command(name="customEmbed", guild=guild_id1)
async def embedtest(interaction: discord.Interaction, url: str):
    TestVideoEmbed = {}
    TestVideoEmbed['type'] = 'video'
    TestVideoEmbed['url'] = url
    VideoDict = {}
    VideoDict['height'] = 480
    VideoDict['proxy_url'] = f'https://images-ext-1.discordapp.net/external/Tr36h2z0bxXh1JF-DYH6igRBj9SClhe_b1sxIF8CvgA/{url}'
    VideoDict['url'] = url
    VideoDict['width'] = 480
    TestVideoEmbed['video'] = VideoDict
    CreatedEmbed = discord.Embed.from_dict(TestVideoEmbed)
    await interaction.response.send_message(embed=CreatedEmbed)

#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + "| Build Infos |" + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
client.run(str(DISCORD_TOKEN))