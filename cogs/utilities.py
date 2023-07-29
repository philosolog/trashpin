import discord
from discord.ext import commands
from decimal import Decimal

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command()
	async def help(self, ctx: discord.ApplicationContext):
		"""see what i can do"""
		await ctx.respond("# just pin something and see")
	@commands.slash_command()
	async def ping(self, ctx: discord.ApplicationContext):
		"""view my latency"""
		await ctx.respond(f"# returned in {round(Decimal(self.bot.latency*1000))}ms")


def setup(bot):
	bot.add_cog(utilities(bot))