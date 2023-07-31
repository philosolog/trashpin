import discord
import datetime
import time
import sqlite3
import settings
from discord.ext import commands

class archiver(discord.Cog, name="archiver"):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_message_edit(self, before, after): # TODO: Add channel-ignoring utility.
		if after.pinned == True:
			guilds = sqlite3.connect(settings.guilds_directory)
			guilds_cursor = guilds.cursor()
			archive_channel = None
			embed = discord.Embed(
				description=after.content,
				color=0x7289da,
				timestamp=datetime.datetime.utcfromtimestamp(int(time.time()))
			)

			embed.set_author(
				name=after.author.display_name,
				icon_url=after.author.display_avatar.url,
				url=f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}"
			)

			if after.attachments:
				embed.set_image(url=after.attachments[0].url)

			embed.set_footer(text=f"#{after.channel}")

			try:
				archive_channel_id = guilds_cursor.execute("select archive_channel_id from guilds where guild_id = ?", (after.guild.id,)).fetchone()[0]

				archive_channel = self.bot.get_channel(archive_channel_id)
			except TypeError: # ?: Is it correct to use TypeError?
				pass

			guilds_cursor.close()
			guilds.close()

			try:
				await archive_channel.send(
					content=f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id} pinned by [pinner]",
					embed=embed,
					silent=True
				) # TODO: Ping who pinned; RETHINK if it is necessary for silent=True...
			except:
				pass

			pass

def setup(bot):
	bot.add_cog(archiver(bot))