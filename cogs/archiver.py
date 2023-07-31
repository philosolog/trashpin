import discord
import datetime
import time
from discord.ext import commands

class archiver(discord.Cog, name="archiver"):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if after.pinned == True:
			embed = discord.Embed(
				description=after.content,
				color=0x7289da,
				timestamp=datetime.datetime.utcfromtimestamp(int(time.time()))
			)
			embed.set_author(
				name=after.author.display_name,
				icon_url=after.author.display_avatar.url,
			)

			if after.attachments:
				embed.set_image(url=after.attachments[0].url)

			embed.set_footer(text=f"#{after.channel}")

			channel = self.bot.get_channel(1134917801732227072) # TODO: Save channels per server.
			await channel.send(
				content=f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id} by {after.author.mention}",
				embed=embed,
				silent=True
			) # TODO: Ping who pinned; RETHINK if it is necessary for silent=True...

def setup(bot):
	bot.add_cog(archiver(bot))