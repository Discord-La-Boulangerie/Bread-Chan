

# @client.tree.command(name="get_partner_invite", description="permet d'obtenir l'accès à un serveur parmi ceux du bot")
# @app_commands.autocomplete(guild=public_autocomplete)
# @app_commands.rename(guild="serveur")
# async def invite_serv(interaction: discord.Interaction, guild: str):
#     gld = discord.utils.get(client.guilds, name=guild)

#     if gld is None:
#         await interaction.response.send_message("Le serveur spécifié n'a pas été trouvé.", ephemeral=True)
#         return

#     try:
#         timeout = 120
#         invited = await gld.text_channels[0].create_invite(max_uses=1, max_age=timeout)
#         time_delete = dat.datetime.now() + dat.timedelta(seconds=timeout)
#         time_delete_totimestamp = round(time_delete.timestamp())
#         await interaction.response.send_message(f"Voici le lien d'invitation pour \"{guild}\". il expirera dans <t:{time_delete_totimestamp}:R>: {invited}", ephemeral=True)
#     except discord.errors.Forbidden:
#         await interaction.response.send_message("Je n'ai pas la permission de créer des invitations dans ce serveur.", ephemeral=True)
#     except discord.errors.DiscordException as e:
#         await interaction.response.send_message(f"Une erreur s'est produite : {e}", ephemeral=True)


# @configGroup.command(name='word-react', description='Configuration du système de reactions de mots')
# async def config_word_react(interaction: discord.Interaction, enabled: Optional[bool]):
#     msg = ""

#     credentials: Credentials = sensitiveClass.get_db_credentials()
#     connexion = db.connect(**credentials.to_dict())
#     curseur = connexion.cursor()
#     if interaction.guild:
#         if isinstance(enabled, bool):
#             curseur.execute(
#                 f"UPDATE guild_config SET word_react_enabled = {int(enabled)} WHERE guild_id = {interaction.guild.id}")
#             msg = "système de word react activé avec succès !"
#             connexion.commit()

#         else:
#             curseur.execute(
#                 "SELECT word_react_enabled FROM guild_config WHERE guild_id = ?", [interaction.guild.id])
#             result: Any = curseur.fetchone()
#             if result:
#                 msg = f"configuration actuelle :\nWord react : ``{result[0]}``"
#             else:
#                 msg = "hmmm... tu n'etais pas sensé voir ca."

#     await interaction.response.send_message(msg, ephemeral=True)

#     if connexion:
#         curseur.close()
#         connexion.close()


# @configGroup.command(name="welcome", description="Configuration du système de bienvenue")
# @app_commands.rename(option="chat", enabled="activé", img_url="image")
# @app_commands.choices(option=[
#     app_commands.Choice(name="Salon de bienvenue", value="welcome_ID"),
#     app_commands.Choice(name="Message de bienvenue", value="welcome_MSG"),
#     app_commands.Choice(name="Définir les deux", value="welcome_ID_&_MSG")
# ])
# async def config_welc(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]] = None, enabled: Optional[bool] = True, img_url: Optional[str] = None):
#     if client.user and interaction.guild and client.application:
#         owner = client.get_user(client.application.owner.id)
#         if isinstance(owner, discord.User):

#             # Connexion à la base de données
#             credentials: Credentials = sensitiveClass.get_db_credentials()
#             connexion = db.connect(**credentials.to_dict())

#             emb = discord.Embed(
#                 title="config_welcome : configuration actuelle")
#             emb.set_author(name=client.user.display_name,
#                            url=f"https://discord.com/users/{client.user.id}", icon_url=client.user.display_avatar.url)

#             if option is None and enabled is True and img_url is None:
#                 select_request = "SELECT welcome_channel_id, welcome_message, enabled, img_url FROM guild_welc where guild_id = ?"
#                 curseur = connexion.cursor()
#                 curseur.execute(select_request, [interaction.guild.id])
#                 result: Any = curseur.fetchone()
#                 if result and isinstance(result, tuple):
#                     await owner.send(f'result1 = {result}')
#                     img = result[3]
#                     activated = str(bool(result[2])).replace(
#                         'True', 'Oui').replace('False', 'Non')
#                     img_txt = " Aucune image de bienvenue n\'a été définie" if str(
#                         img) == 'None' else ''
#                     channel = interaction.guild.get_channel(result[0])
#                     emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
#                     log(img)
#                     if str(img) != "None":
#                         emb.set_image(url=img)
#                     await interaction.response.send_message(embed=emb, ephemeral=True)
#                 else:
#                     await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
#                 curseur.close()
#             else:
#                 style = discord.TextStyle.paragraph
#                 lenght = 0
#                 if option is not None and option.value != 'welcome_ID_&_MSG':
#                     if option.value == "welcome_ID":
#                         lenght = 20
#                         style = discord.TextStyle.short
#                     elif option.value == "welcome_MSG":
#                         lenght = 4000
#                         style = discord.TextStyle.long
#                     await interaction.response.send_modal(ClassModule.WelcomeModal(option.value, lenght, style, enabled, img_url))
#                 else:
#                     await interaction.response.send_modal(ClassModule.WelcomeModal(option.value if option is not None else "Modal", lenght, style, enabled, img_url))
#                 await owner.send(f"{option} {enabled} {img_url}")
#             connexion.close()


# @configGroup.command(name="goodbye", description="Configuration du système de départs")
# @app_commands.rename(option="chat", enabled="activé", img_url="image")
# @app_commands.choices(option=[
#     app_commands.Choice(name="Salon de départ", value="bye_ID"),
#     app_commands.Choice(name="Message de départ", value="bye_MSG"),
#     app_commands.Choice(name="Définir les deux", value="bye_ID_&_MSG")
# ])
# async def config_bye(interaction: discord.Interaction, option: Optional[app_commands.Choice[str]], enabled: Optional[bool], img_url: Optional[str]):
#     import ClassModule
#     app = interaction.client.application
#     if app and interaction.guild and client.user:
#         owner = interaction.client.get_user(app.owner.id)
#         if isinstance(owner, discord.User):

#             # Connexion à la base de données
#             credentials: Credentials = sensitiveClass.get_db_credentials()
#             connexion = db.connect(**credentials.to_dict())

#             emb = discord.Embed(
#                 title="config_goodbye : configuration actuelle")
#             usr = client.user
#             if usr:
#                 emb.set_author(
#                     name=usr.display_name, url=f"https://discord.com/users/{client.user.id}", icon_url=usr.display_avatar.url)

#             if option is None and enabled is True and img_url is None:
#                 select_request = f"SELECT goodbye_channel_id, goodbye_message, enabled, img_url FROM guild_bye where guild_id = {interaction.guild.id}"
#                 curseur = connexion.cursor()
#                 curseur.execute(select_request)
#                 result: Any = curseur.fetchone()
#                 if result and isinstance(result, tuple):
#                     await owner.send(f'result1 = {result}')
#                     img = result[3]
#                     activated = str(bool(result[2])).replace(
#                         'True', 'Oui').replace('False', 'Non')
#                     img_txt = " Aucune image de départ n\'a été définie" if str(
#                         img) == 'None' else ''
#                     if interaction.guild:
#                         channel = interaction.guild.get_channel(result[0])
#                     emb.description = f"Configuration actuelle :\nSalon d'annonce : {channel.mention if channel is not None else ''}\nMessage d'annonce : {result[1]}\nActivé : {activated}\nImage :{img_txt}"
#                     log(img)
#                     if str(img) != "None":
#                         emb.set_image(url=img)
#                     await interaction.response.send_message(embed=emb, ephemeral=True)
#                 else:
#                     await interaction.response.send_message("Le système n'a pas encore été configuré sur ce serveur.", ephemeral=True)
#                 curseur.close()
#             else:
#                 style = discord.TextStyle.paragraph
#                 lenght = 0
#                 if option is not None and option.value != 'bye_ID_&_MSG':
#                     if option.value == "bye_ID":
#                         lenght = 20
#                         style = discord.TextStyle.short
#                     elif option.value == "bye_MSG":
#                         lenght = 4000
#                         style = discord.TextStyle.long
#                     await interaction.response.send_modal(ClassModule.ByeModal(option.value, lenght, style, enabled, img_url))
#                 else:
#                     await interaction.response.send_modal(ClassModule.ByeModal(option.value if option is not None else "Modal", lenght, style, enabled, img_url))
#                 await owner.send(f"{option} {enabled} {img_url}")
#             connexion.close()


# @configGroup.command(name='one-msg-chat', description='configuration du chat autorisant un seul msg')
# async def one_msg_chat(interaction: discord.Interaction, channel: Optional[discord.TextChannel], enabled: Optional[bool], role: Optional[discord.Role]):
#     if interaction.guild:
#         msg = ""
#         connexion = db.connect(**sensitiveClass.get_db_credentials())
#         cursor = connexion.cursor()
#         if all([channel == None, enabled == None, role == None]) is True:
#             request = f"SELECT one_msg_channel, one_msg_role_id, one_msg_enabled FROM guild_config WHERE guild_id = {interaction.guild.id}"
#             cursor.execute(request)
#             result: Any = cursor.fetchone()
#             if all([result[0] == 0, result[1] == 0, bool(result[2]) == False]):
#                 msg = "aucun chat n'a été configuré pour ce système."
#             elif interaction.guild:
#                 unSalon = interaction.guild.get_channel(result[0])
#                 unRole = interaction.guild.get_role(result[1])
#                 if unSalon and unRole:

#                     msg = f"voici la configuration actuelle :\n\nSalon : {unSalon.mention if result[0] is not None else 'aucun'}\n\nRôle : {unRole.mention if result[1] is not None else 'aucun'}\n\nActivé : {bool(result[2])}"
#         else:
#             request = f"UPDATE guild_config SET one_msg_channel = {channel.id if channel is not None else 0}, one_msg_enabled = {enabled}, one_msg_role_id = {role.id if role is not None else 0} WHERE guild_id = {interaction.guild.id}"
#             try:
#                 cursor.execute(request)
#             except db.DatabaseError as dberr:
#                 msg = f"une erreur est survenue lors de la connexion à la base de données : {dberr}"
#             else:
#                 if channel:
#                     msg = f"la configuration actuelle a été mise à jour !\n\nSalon : {channel.mention}"
#         await interaction.response.send_message(msg, ephemeral=True)


# # @configGroup.command(name="auto-role", description="configuration des rôles automatiques")
# # async def auto_role_setup(interaction: discord.Interaction, role_1: Optional[discord.Role] = None, role_2: Optional[discord.Role] = None, role_3: Optional[discord.Role] = None, role_4: Optional[discord.Role] = None, enabled: bool = True):
# #     if all(role is None for role in [role_1, role_2, role_3, role_4]) and interaction.guild:
# #         request = f'SELECT role_1 FROM auto_roles WHERE guild_id = {interaction.guild.id}'
# #     if interaction.guild and role_1 != None:

# #         # Connexion à la base de données
# #         connexion = db.connect(**sensitiveClass.get_db_credentials())

# #         request = f"SELECT enabled FROM auto_roles WHERE guild_id = {interaction.guild.id}"
# #         curseur = connexion.cursor()
# #         curseur.execute(request)
# #         result: Any = curseur.fetchall()
# #         log(result)
# #         if result:
# #             if result[0][0] == None:
# #                 base_request = "INSERT INTO auto_roles (guild_id, role_1"
# #                 values = [interaction.guild.id, role_1.id]

# #                 base_request_2 = ""
# #                 base_request_3 = ""
# #                 base_request_4 = ""

# #                 request_mid = ", enabled) VALUES (" + \
# #                     ", ".join(map(str, values))
# #                 request_2 = ""
# #                 request_3 = ""
# #                 request_4 = ""
# #                 request_5 = ""
# #                 request_end = ")"

# #                 if role_2 is not None:
# #                     base_request += ", role_2"
# #                     values.append(role_2.id)
# #                     request_2 = f", {role_2.id}"

# #                 if role_3 is not None:
# #                     base_request += ", role_3"
# #                     values.append(role_3.id)
# #                     request_3 = f", {role_3.id}"

# #                 if role_4 is not None:
# #                     base_request += ", role_4"
# #                     values.append(role_4.id)
# #                     request_4 = f", {role_4.id}"

# #                 request = base_request + base_request_2 + base_request_3 + base_request_4 + \
# #                     request_mid + request_2 + request_3 + request_4 + request_5 + request_end

# #                 log(request)

# #         else:
# #             base_request = f"UPDATE auto_roles SET role_1 = {role_1.id}"
# #             values = []

# #             base_request_2 = ""
# #             base_request_3 = ""
# #             base_request_4 = ""

# #             request_end = f" WHERE guild_id = {interaction.guild.id}"

# #             if role_2 is not None:
# #                 base_request += f", role_2"
# #                 values.append(role_2.id)
# #             else:
# #                 base_request += f", role_2 = NULL"

# #             if role_3 is not None:
# #                 base_request += f", role_3"
# #                 values.append(role_3.id)
# #             else:
# #                 base_request += f", role_3 = NULL"

# #             if role_4 is not None:
# #                 base_request += f", role_4"
# #                 values.append(role_4.id)
# #             else:
# #                 base_request += f", role_4 = NULL"

# #             if enabled is not None:
# #                 base_request += f", enabled"
# #                 values.append(enabled)
# #             else:
# #                 base_request += f", enabled = NULL"

# #             request = base_request + request_end

# #             log(request)
# #         try:
# #             curseur.execute(request)
# #         except Exception as e:
# #
# #         await interaction.response.send_message("le système d'auto roles pour ce serveur a été configuré avec succès", ephemeral=True)
# #         # Fermeture de la connexion et commit
# #         connexion.commit()
# #         connexion.close()
