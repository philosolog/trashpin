import discord
from discord.ext import commands

class archiver(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	
	


def setup(bot):
	bot.add_cog(archiver(bot))
