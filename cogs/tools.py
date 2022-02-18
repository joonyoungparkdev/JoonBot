import time

from discord.ext import commands


class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pang!')

    @commands.command()
    async def echo(self, ctx, *, args):
        await ctx.send(args)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    async def countdown(self, ctx, minutes=0, *, args):
        sender = ctx.message.author
        await ctx.channel.send('Timer started for ' + minutes + ' minutes')

        if minutes > 0:
            time.sleep(int(minutes * 60))
            await ctx.channel.send('Time is up ' + sender.mention + args)

    @commands.command(aliases=['renameRole'])
    async def rename(self, ctx):
        sender = ctx.message.author
        roles = sender.roles
        print(roles)


def setup(client):
    client.add_cog(Tools(client))
