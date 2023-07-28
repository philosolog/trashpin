# @bot.slash_command(name="ping")
# async def global_command(ctx: discord.ApplicationContext):
# 	await ctx.respond(f"# returned in {round(Decimal(bot.latency*1000), 3)}ms")

import discord
from discord.ext import commands
from decimal import Decimal

class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond("# ill add pinging later")


def setup(bot):
    bot.add_cog(utilities(bot))
