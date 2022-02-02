from discord.ext import commands


class DownBad(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.id == "932028197162328114":
            print("hit")


def setup(client):
    client.add_cog(DownBad(client))
