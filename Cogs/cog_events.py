import asyncio
import datetime as dat
import random
import re
from typing import Any, Optional

import discord
from discord.ext import commands
from sqlalchemy import Select, select
import sqlalchemy

import TasksModule
from ClassModule import sensitiveClass
from dataclass.dbTypes import GuildConfig
from sysModule import log


class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_error(self, event: discord.app_commands.AppCommandError, *args, **kwargs):
        log(f"{dat.datetime.now().time()} | {event}")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.client.user:
            log(f"Connecté en tant que {self.client.user.name} (ID: {self.client.user.id})")
            sensitiveClass.initialize_db(self.client)
            try:
                await TasksModule.ReloadPresence.start(self.client)
            except Exception as err:
                log(err)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.client.user:
            # variables definitions
            casefoldMsg = message.content.casefold()
        owner_id = 911467405115535411
        owner = self.client.get_user(owner_id)
        listeMotsReact = [".tiktok.com/",
                          ":moyai:", "quoi", self.client.user.mention]
        randomAnswers = ["https://didnt-a.sk/", "https://tenor.com/bJniJ.gif", "[ok](https://cdn.discordapp.com/attachments/1139849206308278364/1142583449530683462/videoplayback.mp4)",
                         "[.](https://cdn.discordapp.com/attachments/1130945537907114145/1139100471907336243/Untitled_video_-_Made_with_Clipchamp.mp4)", "tg"]

        # functions definitions
        async def send_typing_sleep_reply(content: str, typing_time: float = 1, /, file: Optional[discord.File] = None):
            async with message.channel.typing():
                await asyncio.sleep(typing_time)
            if file:
                await message.reply(content, file=file)
            else:
                await message.reply(content)

        async def search_regular_str(value: str, string: str):
            phrase = string

            # Utilisation d'une expression régulière pour rechercher du texte en tant que mot distinct
            mot_a_chercher = value
            expression_reguliere = fr"\b{re.escape(mot_a_chercher)}\b"

            if re.search(expression_reguliere, phrase, re.IGNORECASE):
                return True
            else:
                return False

        async def tiktokResolver(message: discord.Message):
            log("lien tiktok trouvé, résolution...")
            vxtiktok_resolver = message.content.replace(
                "tiktok.com/", "vxtiktok.com/")
            log("lien tiktok résolu !")
            return vxtiktok_resolver

        if message.author.bot == False:
            try:
                # Connexion à la base de données
                credentials_provider = sensitiveClass.get_db_credentials()
                if credentials_provider:
                    engine = sqlalchemy.create_engine(
                        f"mariadb+mariadbconnector://{credentials_provider.user}:{credentials_provider.password}@{credentials_provider.host}:{credentials_provider.port}/{credentials_provider.database}")
                    session = sqlalchemy.Session(engine)
            except Exception as e:
                log(e)
            else:
                msgGuild = message.guild
                if msgGuild:
                    select_request = select(GuildConfig.word_react_enabled).where(
                        GuildConfig.guild_id == message.guild.id)
                    for result in session.scalars(select_request):

                        if all([result, bool(result[0]) == True, result[1] != 0, result[2] != 0]):
                            if message.channel.id == int(result[1]) and isinstance(message.author, discord.Member):
                                await message.author.add_roles([discord.Object(id=int(result[2]))])

                            if await search_regular_str("bite", casefoldMsg) == True:
                                await send_typing_sleep_reply("https://cdn.discordapp.com/attachments/778672634387890196/1142544668488368208/nice_cock-1.mp4", 2)

                            elif await search_regular_str("uwu", casefoldMsg) == True:
                                await message.add_reaction("<a:DiscordUwU:1209854758282596352>")

                            elif casefoldMsg.startswith("t'as les cramptés ?"):
                                await send_typing_sleep_reply(random.choice(randomAnswers))

                            for i in listeMotsReact:
                                if i in casefoldMsg:
                                    if listeMotsReact[0] and isinstance(message.channel, discord.TextChannel):
                                        vxtiktok_resolver = await tiktokResolver(message)
                                        try:
                                            authorAvatar = message.author.avatar
                                            if authorAvatar:
                                                webhook = await message.channel.create_webhook(name=message.author.display_name, avatar=await authorAvatar.read())
                                        except discord.errors.HTTPException as http_err:
                                            log(http_err)
                                        else:
                                            log("webhook créé !")
                                            await webhook.send(vxtiktok_resolver)
                                            log("message envoyé par le webhook !")
                                            await message.delete()
                                            log("message supprimé !")
                                            await webhook.delete()
                                            log("webhook supprimé !")
                                    if await search_regular_str(listeMotsReact[2], casefoldMsg) == True and message.author.id != owner_id:
                                        await send_typing_sleep_reply("coubaka! UwU")
                                    if casefoldMsg.startswith(listeMotsReact[3]) and message.author.id != owner_id:
                                        await send_typing_sleep_reply(random.choice(["https://cdn.discordapp.com/attachments/928389065760464946/1131347327416795276/IMG_20210216_162154.png"]), 1)
                                    if listeMotsReact[1] in casefoldMsg:
                                        await message.reply("https://canary.discord.com/store/skus/1037148024792690708/moai")

                        elif isinstance(message.channel, discord.TextChannel) and "memes" in message.channel.name.casefold() and message.attachments and random.randint(1, 50) == 1:
                            await message.add_reaction(random.choice(self.client.emojis))

                        elif message.guild and message.guild.id == 1181845184288411688 and message.channel.type == discord.ChannelType.news:
                            if message.channel.id == 1191490955413553183:
                                err = ""
                                try:
                                    await message.create_thread(name=f"Annonce de {message.author.name}")
                                except discord.DiscordException as discordExc:
                                    err = str(discordExc)
                                try:
                                    await message.publish()
                                except discord.DiscordException as discordExc:
                                    err = str(discordExc)
                                if owner:
                                    await owner.send(content=str(err))


async def setup(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))
