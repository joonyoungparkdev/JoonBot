import discord
from discord.ext import commands


class Startup(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def echo(self, ctx, output=""):
        await ctx.send(output)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)


def setup(client):
    client.add_cog(Startup(client))
