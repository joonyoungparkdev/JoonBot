import discord
import time

from discord.ext import commands


class Startup(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def echo(self, ctx, *, args):
        await ctx.send(args)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    async def countdown(self, ctx, minutes):
        time.sleep(int(minutes)*60)
        await ctx.send('Time is up')


def setup(client):
    client.add_cog(Startup(client))
