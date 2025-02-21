import discord
import enka

class EnkaCharactersDropdown(discord.ui.Select):
    async def __init__(self, user_id: int, enka: enka.HSRClient):
        self.user_id = user_id
        options: list[discord.SelectOption] = []
        async with enka:
            showcase = await enka.fetch_showcase(self.user_id)
        if showcase.owner is not None:
            self.owner = showcase.owner
            async with enka:
                character_builds = await enka.fetch_builds(self.owner)
                builds = [build[0] for _, build in character_builds.items()]
                self.builds = builds
            options.extend([discord.SelectOption(
                    label=build.character.name, value=str(build.id)) for build in builds])

        super().__init__(placeholder="Sélectionnez un personnage", max_values=1, min_values=1, options=options)


    async def callback(self, interaction: discord.Interaction):
        emb = discord.Embed(title=f"profil de {self.owner.username} - build de {self.values[0]}")
        selected_build = None
        for build in self.builds:
            if build.id == self.values[0]:
                selected_build = build
                break
        emb.set_thumbnail(url=selected_build.character.icon.card)
        await interaction.response.send_message(embed=emb)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180, user_id: int, enka: enka.HSRClient):
        super().__init__(timeout=timeout)
        self.add_item(EnkaCharactersDropdown(user_id, enka))
