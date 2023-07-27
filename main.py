import discord
import os
import pathlib
import glob
from dotenv import load_dotenv
from pathlib import Path
from decimal import Decimal

base_dir = pathlib.Path(__file__).parent

load_dotenv()

if Path("alternate.env"):
	load_dotenv(Path("alternate.env"))

token = os.getenv("TOKEN_ALTERNATE") or os.getenv("TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
	print(f"User: {bot.user} (ID: {bot.user.id})")
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("with pins.."))

	# load cogs
	for cog_file in glob.glob("cogs/*.py"):
		if cog_file.name != "__init__.py":
			await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

@bot.command(name="help", description="a bit of what i can do")
async def help(ctx):
	await ctx.respond("# just pin something")
@bot.command(name="ping", description="checks my latency") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"# returned in {round(Decimal(bot.latency*1000), 3)}ms")

bot.run(token)