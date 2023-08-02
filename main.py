import discord
import settings
from discord.ext import commands

def main():
	intents = discord.Intents.default()
	intents.members = True
	intents.message_content = True # ?: Is this necessary? # TODO: Add permissions to any channel specified? A confirmation to add permissions to the bot..?
	bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
	bot.remove_command("help")

	for cog_file in settings.cogs_directory.glob("*.py"):
		if cog_file.name != "__init__.py":
			bot.load_extension(f"cogs.{cog_file.name[:-3]}")
			print("cog loaded: " + cog_file.name)

	@bot.event
	async def on_ready():
		print(f"{bot.user} ({bot.user.id}) ready.")

		await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=" pins"))
	bot.run(settings.token)

if __name__ == "__main__":
	main()