import discord
from discord.ext import commands
from discord.utils import get


class Scanner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, payload: discord.Message):
        if 'apex legends' in payload.content.lower():
            print("Found!")
            await payload.channel.send(":poop:")
        print(payload.content)


def setup(client):
    client.add_cog(Scanner(client))

