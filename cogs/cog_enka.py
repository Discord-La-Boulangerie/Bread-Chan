import discord
import enka
import enka.enums
from discord import app_commands
from discord.ext import commands

from datatypes.enka import SelectView


class EnkaGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="enka", description="gestion des roles utilisateurs")
        self.enka = enka.HSRClient(enka.hsr.Language.FRENCH)

    @app_commands.command(name="search", description="recherche un utilisateur")
    async def search_user(self, interaction: discord.Interaction, user: str):
        """Recherche un utilisateur par nom."""
        async with self.enka:
            try:
                showcase = await self.enka.fetch_showcase(user)
            except (enka.errors.EnkaPyError, enka.errors.EnkaAPIError):
                await interaction.response.send_message("Utilisateur introuvable.")
                return
            emb = discord.Embed(title="Recherche d'utilisateur",
                                    description=f"Recherche de l'utilisateur {showcase.player.nickname}")
            emb.set_author(name=showcase.player.nickname,
                               icon_url=showcase.player.icon)
            emb.add_field(name="Niveau", value=showcase.player.level)
            await interaction.response.send_message(embed=emb, view=SelectView(user_id=showcase.player.uid, enka=self.enka))


class EnkaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.enka_group = EnkaGroup()
        self.client.tree.add_command(self.enka_group)


async def setup(bot: commands.Bot):
    await bot.add_cog(EnkaCog(bot))
