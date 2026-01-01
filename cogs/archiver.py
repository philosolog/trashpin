"""Archiver cog for the Trashpin Discord bot.

This module handles archiving pinned messages to a designated channel.
"""

import logging
import sqlite3

import discord
from discord.ext import commands

import settings

logger = logging.getLogger(__name__)


class ArchiverCog(commands.Cog):
	"""Cog that archives pinned messages to a designated channel."""

	def __init__(self, bot: discord.Bot) -> None:
		"""Initialize the archiver cog.

		Args:
			bot: The Discord bot instance.
		"""
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
		"""Handle message edits to detect newly pinned messages.

		Args:
			before: The message before the edit.
			after: The message after the edit.
		"""
		if not after.pinned:
			return

		if after.guild is None:
			return

		guilds = sqlite3.connect(settings.guilds_directory)
		guilds_cursor = guilds.cursor()
		archive_channel: discord.TextChannel | None = None

		embed = discord.Embed(
			description=after.content,
			color=0x7289DA,
			timestamp=before.created_at,
		)

		embed.set_author(
			name=after.author.display_name,
			icon_url=after.author.display_avatar.url,
			url=f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}",
		)

		if after.attachments:
			embed.set_image(url=after.attachments[0].url)

		embed.set_footer(text=f"#{after.channel}")

		try:
			result = guilds_cursor.execute(
				"SELECT archive_channel_id FROM guilds WHERE guild_id = ?",
				(after.guild.id,),
			).fetchone()

			if result and result[0]:
				archive_channel = self.bot.get_channel(result[0])
		except sqlite3.Error:
			logger.exception("Failed to query archive channel for guild %s", after.guild.id)

		guilds_cursor.close()
		guilds.close()

		if archive_channel is None:
			return

		try:
			await archive_channel.send(
				content=f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}",
				embed=embed,
				silent=True,
			)
			logger.info("Archived pin from #%s to #%s", after.channel, archive_channel)
		except discord.DiscordException:
			logger.exception("Failed to send archived pin to channel %s", archive_channel.id)


def setup(bot: discord.Bot) -> None:
	"""Set up the archiver cog.

	Args:
		bot: The Discord bot instance.
	"""
	bot.add_cog(ArchiverCog(bot))