import json
import os
from typing import Any
import discord
from discord.ext import commands
from discord import Permissions, app_commands
from discord.app_commands import locale_str as locale
import datetime as dat
from ClassModule import LoginModal, SensitveClass
import mysql.connector as db

sensitiveClass = SensitveClass()


class UserGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="user", description=locale("configuration du profil des utilisateurs"))

    @app_commands.command(name="setup", description=locale("configurez votre profil"))
    async def profil_setup(self, interaction: discord.Interaction, bio: str):
        msg = ""
        connexion = db.connect(**sensitiveClass.get_db_credentials())
        cursor = connexion.cursor()
        request = f"SELECT user_description FROM user_profile WHERE user_id = {interaction.user.id}"
        cursor.execute(request)
        result: Any = cursor.fetchone()
        if result != None:
            request = f"UPDATE user_profile SET user_description = '{bio}' WHERE user_id = {interaction.user.id}"
            msg = "votre profil utilisateur a été mis à jour."
        else:
            request = f"INSERT INTO user_profile (user_id, user_description) VALUES ({interaction.user.id}, '{bio}')"
            msg = "votre profil utilisateur a été créé avec succès !"
        try:
            cursor.execute(request)
        except Exception as err:
            msg = str(err)
        finally:
            await interaction.response.send_message(msg, ephemeral=True)
            connexion.commit()
            connexion.close()

class UserCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.warframe_group = UserGroup()
        self.client.tree.add_command(self.warframe_group)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserCog(bot))