import discord
from discord.ext import commands

from src import config

TOKEN = config.DISCORD_BOT_TOKEN
PREFIX = '/'
intents = discord.Intents().all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)