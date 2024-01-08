from io import BufferedIOBase
import sys
import os
from dotenv import load_dotenv

# import des API
import enkanetwork as enk
import discord
from discord import VoiceClient, app_commands
import youtube_dl
from discord import FFmpegPCMAudio


load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")

guild_id = 1001496918343553094
guild_id1 = discord.Object(id=guild_id)
intents = discord.Intents.all()

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
        await self.tree.sync(guild=guild_id1)
        await self.tree.sync()

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user.name}')

@client.tree.command(name="connect", guild=guild_id1)
async def join(interaction: discord.Interaction):
    # Vérifie si l'utilisateur est dans un canal vocal
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if channel:
            try:
                # Rejoint le canal vocal
                await channel.connect(self_deaf=True)
            except Exception:
                await interaction.response.send_message("je n'ai pas pu me connecter. :(")
            else:
                await interaction.response.send_message("Je suis connectée !")
        else:
            await interaction.response.send_message("Vous devez être dans un chat vocal pour utiliser cette commande.")
    else:
        await interaction.response.send_message("Vous devez être dans un chat vocal pour utiliser cette commande.")


@client.tree.command(name="disconnect", guild=guild_id1)
async def leave(interaction: discord.Interaction):
    user_channel = interaction.user.voice.channel
    for voice_client in client.voice_clients:
        if voice_client.channel == user_channel:
            try:
                await voice_client.disconnect(force=True)
            except Exception:
                await interaction.response.send_message("Je n'ai pas pu me déconnecter. :(")
            else:
                await interaction.response.send_message("Je suis déconnectée !")
            break

from discord import FFmpegPCMAudio, VoiceClient
from discord.ext import commands

@client.tree.command(name="play", guild=guild_id1)
async def play(interaction: discord.Interaction, file: discord.Attachment):
    def trash_remover(url: str):
        print(url)
        url, buffer = url.split("?ex=")
        print(url)
        return url

    async def music_play(voice_channel: VoiceClient, url: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        clear = trash_remover(url)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clear, download=False)
            print(info)
            url2 = info['formats'][0]['url']
            print(url2)

        if voice_channel is not None:
            # Jouer l'audio dans le canal vocal
            voice_channel.play(FFmpegPCMAudio(url2, executable="C:/Users/conta/Documents/GitHub/Bread-Chan/final/BC/ffmpeg.exe"))

    user_channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if not user_channel:
        await interaction.response.send_message("Vous devez être dans un canal vocal pour utiliser cette commande.")
        return

    if voice_client:
        # Si le bot est déjà connecté à un canal vocal
        if voice_client.channel != user_channel:
            await voice_client.disconnect()
            await user_channel.connect(self_deaf=True)
    else:
        # Si le bot n'est pas déjà connecté, connectez-le
        voice_client = await user_channel.connect()

    # Télécharger les informations audio à partir du fichier .mp3
    await music_play(voice_client, file.url)
    await interaction.response.send_message(f"Now playing: {file.filename}")


client.run(str(DISCORD_TOKEN))