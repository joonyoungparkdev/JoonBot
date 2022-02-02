from discord.ext import commands
from discord.utils import get


class Comment(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def yourself(self, ctx):
        await ctx.send('https://tenor.com/view/congrats-djkhlaed-player-yourself-foolingyourself-gif-4961672')

    @commands.command(aliases=['fuck', 'fuckthisshit'])
    async def curse(self, ctx):
        await ctx.send("THAT'S RIGHT, FUCK THIS SHIT")

    @commands.command(aliases=['letsfuckinggo'])
    async def lfg(self, ctx):
        await ctx.send("LET'S FUCKING GO!")
        await ctx.send("https://tenor.com/view/lfg-ruj-tits-lets-fucking-go-lets-go-gif-15383476")

    @commands.command(aliases=['whereheat'])
    async def where(self, ctx):
        await ctx.send("https://memegenerator.net/img/instances/61599036.jpg")

    @commands.command()
    async def kekw(self, ctx):
        await ctx.send("https://tenor.com/view/kekw-kek-bttv-twitch-emote-gif-15123134")

    @commands.command()
    async def damn(self, ctx):
        await ctx.send("https://tenor.com/view/damn-shookt-shocked-gif-5580082")

    @commands.command()
    async def nice(self, ctx):
        await ctx.send("https://tenor.com/view/noice-nice-click-gif-8843762")

    @commands.command()
    async def calendar(self, ctx):
        await ctx.send("1/10: First Day of Classes\n"
                       "1/17: No School\n"
                       "3/14 - 3/18: Spring Break\n"
                       "5/1 - 5/5 : Finals Week")

    @commands.command()
    async def runit(self, ctx):
        searched_role = get(ctx.guild.roles, name='Radiants')
        await ctx.send(searched_role.mention + " run it?")


def setup(client):
    client.add_cog(Comment(client))
