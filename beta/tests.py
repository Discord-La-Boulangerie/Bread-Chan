import requests, pprint, os, discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from datetime import datetime
TOKEN = "My Bot Token"
headers = {"Authorization": f"Bot {TOKEN}"}
userid = 911467405115535411
req = requests.get(f"https://discord.com/api/v9/users/{userid}", headers=headers)
pprint.pprint(req.json())