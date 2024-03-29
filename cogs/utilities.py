import discord
import sqlite3
import settings
import typing
from discord.ext import commands
from decimal import Decimal

# TODO: Denote the most recent startup and other stats.
class utilities(discord.Cog, name="utilities"):
	def __init__(self, bot):
		self.bot = bot
	@commands.slash_command()
	async def help(self, ctx: discord.ApplicationContext):
		"""see what i can do"""

		await ctx.respond("# just pin something and see", ephemeral=True)
	@commands.slash_command()
	async def ping(self, ctx: discord.ApplicationContext):
		"""view my latency"""

		await ctx.respond(f"# returned in {round(Decimal(self.bot.latency*1000))}ms", ephemeral=True)
	@commands.slash_command()
	async def enable(self, ctx: discord.ApplicationContext, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.ForumChannel]): # ?: Does it error when the first form is not provided? # TODO: Make channel-type messagability checking.
		"""enable my logging (to specified channel)"""
		if ctx.author.guild_permissions.administrator: # TODO: Create a user-necessary permissions list.
			if channel.can_send(): # TODO: Add the checking of permissions.
				guilds = sqlite3.connect(settings.guilds_directory)
				guilds_cursor = guilds.cursor()

				guilds_cursor.execute("INSERT OR REPLACE INTO guilds (guild_id, archive_channel_id) VALUES (?, ?)", (ctx.guild_id, channel.id))
				guilds.commit()
				guilds_cursor.close()
				guilds.close()

				await ctx.respond(f"# pins will now be saved to {channel.mention}", ephemeral=True)
			else:
				await ctx.respond("# i can't send messages to that channel", ephemeral=True)
		else:
			await ctx.respond("# in order to do that, you need `administrator` permissions in the server", ephemeral=True) # TODO: Make this a part of a set of general error messages.
	@commands.slash_command()
	async def disable(self, ctx: discord.ApplicationContext):
		"""disable my logging"""

		guilds = sqlite3.connect(settings.guilds_directory)
		guilds_cursor = guilds.cursor()
		
		try:
			if guilds_cursor.execute("select archive_channel_id from guilds where guild_id = ?", (ctx.guild_id,)).fetchone()[0] == 0:
				await ctx.respond("# pin logging isn't enabled in this server.. try `/enable [channel]` to get started", ephemeral=True)
			else:
				guilds_cursor.execute("INSERT OR REPLACE INTO guilds (guild_id, archive_channel_id) VALUES (?, ?)", (ctx.guild_id, 0))
				guilds.commit()

				await ctx.respond("# pins are no longer being archived ☹", ephemeral=True)
		except:
			await ctx.respond("# pin logging isn't enabled in this server.. try `/enable [channel]` to get started", ephemeral=True)

		guilds_cursor.close()
		guilds.close()

	pass # ?: Necessary?


def setup(bot):
	bot.add_cog(utilities(bot))

# TODO: Make use of an "error" method for other cogs.