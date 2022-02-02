from discord.ext import commands


class Apex(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Apex Legends'])
    async def apex(self, ctx):
        await ctx.send(":dog: :poop: game")

    @commands.command(aliases=['gibby'])
    async def gibraltar(self, ctx):
        await ctx.send("ALL my homies hate Gibby")

    @commands.command()
    async def worldwide(self, ctx):
        await ctx.send("#1 GIBRALTAR WORLDWIDE")

    @commands.command()
    async def loba(self, ctx):
        await ctx.send("Ms. Thiccums")

    @commands.command(aliases=['hound'])
    async def bloodhound(self, ctx):
        await ctx.send("ALLFATHER GIVE ME SIGHT")

    @commands.command()
    async def wraith(self, ctx):
        await ctx.send("shoot this")

    @commands.command(aliases=['bang'])
    async def bangalore(self, ctx):
        await ctx.send("Lock and load, rinse, repeat. It's that simple.")

    @commands.command(aliases=['path'])
    async def pathfinder(self, ctx):
        await ctx.send("Hello Friend :)")

    @commands.command(aliases=['wifeline'])
    async def lifeline(self, ctx):
        await ctx.send("LIFELINEEEE: https://www.youtube.com/watch?v=zZpy5J9w4-M")

    @commands.command(aliases=['ez'])
    async def ezdub(self, ctx):
        await ctx.send(":trophy: :trophy: :trophy: TOO FUCKIN EZ BABY:trophy: :trophy: :trophy: ")

    @commands.command()
    async def beta(self, ctx):
        await ctx.send("https://tenor.com/view/gina-linetti-charles-boyle-alpha-beta-brooklyn99-gif-11868085")

    @commands.command()
    async def play(self, ctx):
        await ctx.send("https://media.tenor.com/images/779cc2cbd0aefd876efa3129130f7c28/tenor.gif")


def setup(client):
    client.add_cog(Apex(client))
