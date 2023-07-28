import discord
import settings
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
bot.remove_command("help")

for cog_file in settings.cogs_directory.glob("*.py"):
	if cog_file.name != "__init__.py":
		bot.load_extension(f"cogs.{cog_file.name[:-3]}")

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game(""))

bot.run(settings.token)