import discord
from discord import app_commands

TOKEN = "your token"


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
    # the method to override in order to run whatever you need before your bot starts

    async def setup_hook(self):
        await self.login(TOKEN)


e = MyClient(intents=discord.Intents.all())
e.login()


ExampleBot().run(TOKEN)
