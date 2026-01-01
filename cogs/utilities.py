"""Utilities cog for the Trashpin Discord bot.

This module provides utility slash commands for help, ping, and enabling/disabling archiving.
"""

import logging
import sqlite3
from decimal import Decimal

import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)


class UtilitiesCog(commands.Cog):
	"""Cog that provides utility slash commands."""

	def __init__(self, bot: discord.Bot) -> None:
		"""Initialize the utilities cog.

		Args:
			bot: The Discord bot instance.
		"""
		self.bot = bot

	@discord.slash_command(
		name="help",
		description="See what I can do",
	)
	async def help_command(self, ctx: discord.ApplicationContext) -> None:
		"""Display help information.

		Args:
			ctx: The application context for the command.
		"""
		await ctx.respond("# just pin something and see", ephemeral=True)

	@discord.slash_command(
		name="ping",
		description="View my latency",
	)
	async def ping_command(self, ctx: discord.ApplicationContext) -> None:
		"""Display bot latency.

		Args:
			ctx: The application context for the command.
		"""
		latency_ms = round(Decimal(self.bot.latency * 1000))
		await ctx.respond(f"# returned in {latency_ms}ms", ephemeral=True)

	@discord.slash_command(
		name="enable",
		description="Enable my logging (to specified channel)",
	)
	async def enable_command(
		self,
		ctx: discord.ApplicationContext,
		channel: discord.TextChannel | discord.VoiceChannel,
	) -> None:
		"""Enable pin archiving to a specified channel.

		Args:
			ctx: The application context for the command.
			channel: The channel to archive pins to.
		"""
		if ctx.author is None or ctx.guild_id is None:
			await ctx.respond("# something went wrong", ephemeral=True)
			return

		# Check for admin permissions
		if isinstance(ctx.author, discord.Member) and not ctx.author.guild_permissions.administrator:
			await ctx.respond(
				"# in order to do that, you need `administrator` permissions in the server",
				ephemeral=True,
			)
			return

		if not channel.can_send():
			await ctx.respond("# i can't send messages to that channel", ephemeral=True)
			return

		guilds = sqlite3.connect(settings.guilds_directory)
		guilds_cursor = guilds.cursor()

		try:
			guilds_cursor.execute(
				"INSERT OR REPLACE INTO guilds (guild_id, archive_channel_id) VALUES (?, ?)",
				(ctx.guild_id, channel.id),
			)
			guilds.commit()
			logger.info("Enabled archiving for guild %s to channel %s", ctx.guild_id, channel.id)
		except sqlite3.Error:
			logger.exception("Failed to enable archiving for guild %s", ctx.guild_id)
			await ctx.respond("# something went wrong", ephemeral=True)
			return
		finally:
			guilds_cursor.close()
			guilds.close()

		await ctx.respond(f"# pins will now be saved to {channel.mention}", ephemeral=True)

	@discord.slash_command(
		name="disable",
		description="Disable my logging",
	)
	async def disable_command(self, ctx: discord.ApplicationContext) -> None:
		"""Disable pin archiving.

		Args:
			ctx: The application context for the command.
		"""
		if ctx.guild_id is None:
			await ctx.respond("# something went wrong", ephemeral=True)
			return

		guilds = sqlite3.connect(settings.guilds_directory)
		guilds_cursor = guilds.cursor()

		try:
			result = guilds_cursor.execute(
				"SELECT archive_channel_id FROM guilds WHERE guild_id = ?",
				(ctx.guild_id,),
			).fetchone()

			if result is None or result[0] == 0:
				await ctx.respond(
					"# pin logging isn't enabled in this server.. try `/enable [channel]` to get started",
					ephemeral=True,
				)
				return

			guilds_cursor.execute(
				"INSERT OR REPLACE INTO guilds (guild_id, archive_channel_id) VALUES (?, ?)",
				(ctx.guild_id, 0),
			)
			guilds.commit()
			logger.info("Disabled archiving for guild %s", ctx.guild_id)
			await ctx.respond("# pins are no longer being archived ☹", ephemeral=True)

		except sqlite3.Error:
			logger.exception("Failed to disable archiving for guild %s", ctx.guild_id)
			await ctx.respond("# something went wrong", ephemeral=True)
		finally:
			guilds_cursor.close()
			guilds.close()


def setup(bot: discord.Bot) -> None:
	"""Set up the utilities cog.

	Args:
		bot: The Discord bot instance.
	"""
	bot.add_cog(UtilitiesCog(bot))