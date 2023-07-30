import discord
import datetime
import time
from discord.ext import commands

class archiver(discord.Cog, name="archiver"):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_edit(self, before, after): # TODO: Refactor this method...
		if after.pinned == True:
			name = after.author.display_name
			avatar = after.author.display_avatar.url
			pin_content = after.content
			server = after.guild.id
			current_date = datetime.datetime.utcfromtimestamp(int(time.time()))
			emb = discord.Embed(
				description=pin_content,
				color=0x7289da,
				timestamp=current_date
			)
			emb.set_author(
				name=name,
				icon_url=avatar,
				# url='https://discordapp.com/channels/{0}/{1}/{2}'.format(server, after.channel.id, after.id)
			)

			if after.attachments:
				img_url = after.attachments[0].url
				emb.set_image(url=img_url)

			emb.set_footer(text='Sent in #{}'.format(after.channel))

			channel = self.bot.get_channel(1134917801732227072) # TODO: Save channels per server.
			await channel.send(content=f"https://discord.com/channels/{server}/{after.channel.id}/{after.id} by {after.author.mention}", embed=emb, silent=True) # TODO: Ping who pinned; RETHINK if it is necessary for silent=True...


def setup(bot):
	bot.add_cog(archiver(bot))