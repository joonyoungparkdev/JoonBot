import discord
from discord.ext import commands


class Comment(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def yourself(self, ctx):
        await ctx.send('https://tenor.com/view/congrats-djkhlaed-player-yourself-foolingyourself-gif-4961672')

    @commands.command(aliases=['fuck', 'fuckthisshit', 'FUCK', 'FUCKTHISSHIT'])
    async def curse(self, ctx):
        await ctx.send("THAT'S RIGHT, FUCK THIS SHIT")

    @commands.command(aliases=['LETSFUCKINGGO', 'letsfuckinggo', 'LFG'])
    async def lfg(self, ctx):
        await ctx.send("LET'S FUCKING GO!")
        await ctx.send("https://tenor.com/view/lfg-ruj-tits-lets-fucking-go-lets-go-gif-15383476")

    @commands.command(aliases=['WHERE', 'whereheat'])
    async def where(self, ctx):
        await ctx.send("https://memegenerator.net/img/instances/61599036.jpg")


def setup(client):
    client.add_cog(Comment(client))