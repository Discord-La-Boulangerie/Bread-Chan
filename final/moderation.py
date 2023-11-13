import discord, datetime

async def banfunct(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.id == member.id:
        await interaction.response.send_message("wtf t'as vraiment pas d'amour propre pour essayer de te ban toi-même ou ca se passe comment ?", ephemeral=True)
    if interaction.user.top_role.position <= member.top_role.position: #type: ignore
        emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de ban {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal à ton rôle le plus haut.", color=discord.Color.dark_embed(), timestamp=datetime.datetime.now())
        await interaction.response.send_message(embed=emb, ephemeral=True) #type: ignore
    else:
        varmonth = datetime.datetime.now() + datetime.timedelta(days=30)
        timestamp = round(varmonth.timestamp())
        await member.send(f"tu as été banni de {interaction.guild.name} pour cette raison : ``{reason}``. tu pourras faire une demande de débanissement le <t:{timestamp}:D>", silent=True)
        if reason == None:
            reason = interaction.user.name + " | a sûrement fait quelque chose d'inacceptable"
            await member.ban(reason=reason)
        else:
            reason = interaction.user.name + " | a sûrement fait quelque chose d'inacceptable"
            await member.ban(reason=reason)

async def mutefunct(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str):
    trueduration = datetime.timedelta(minutes=float(duration))
    if interaction.user.id == member.id:
        await interaction.response.send_message("wtf t'as vraiment pas d'amour propre pour essayer de te mute toi-même ou ca se passe comment ?", ephemeral=True)

    if interaction.user.top_role.position <= member.top_role.position: #type: ignore
        emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal à ton rôle le plus haut.", color=discord.Color.dark_embed(), timestamp=datetime.datetime.now())
        await interaction.response.send_message(embed=emb, ephemeral=True) #type: ignore
    else:
        await member.send(f"tu as été mute {duration} minutes pour la raison suivante : {reason}")
        if reason == None:
            reason = interaction.user.name + "| a sûrement fait quelque chose d'irrespectueux"
            await member.timeout(trueduration, reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute {duration} minutes", ephemeral=True)
        else:
            await member.timeout(trueduration, reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute {duration} minutes", ephemeral=True)


async def kickfunct(interaction: discord.Interaction, member: discord.Member, reason: str):
    if interaction.user.id == member.id:
        await interaction.response.send_message("wtf t'as vraiment pas d'amour propre pour essayer de te kick toi-même ou ca se passe comment ?", ephemeral=True)

    if interaction.user.top_role <= member.top_role: #type: ignore
        emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", color=discord.Color.red()) #type: ignore
        await interaction.response.send_message(embed=emb, ephemeral=True)
    else:
        await member.send(f"tu as été kick pour la raison suivante : {reason}")
        if reason == None:
            reason = interaction.user.name + "| a sûrement fait quelque chose d'irrespectueux"
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.display_name} (id = {member.id}) a bien été kick", ephemeral=True)
        else:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.display_name} (id = {member.id}) a bien été kick", ephemeral=True)