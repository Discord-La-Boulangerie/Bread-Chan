import discord

colorList = [value for value in dir(discord.Color) if not value.startswith('_') and not value.startswith(
    "from") and not value.startswith("to") and not value.startswith('value') and not len(value) <= 1]
for color in colorList:
    print(color)
