import discord
import os
import pathlib
import glob
from dotenv import load_dotenv
from pathlib import Path

base_dir = pathlib.Path(__file__).parent

load_dotenv()

if Path("ignored.env"):
	load_dotenv(Path("ignored.env"))

token = os.getenv("TOKEN_ALTERNATE") or os.getenv("TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("with pins.."))

	# load cogs
	for cog_file in glob.glob("cogs/*.py"):
		if cog_file.name != "__init__.py":
			await bot.load_extension(f"cogs.{cog_file.name[:-3]}")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
	await ctx.respond("Hey!")

bot.run(token)
