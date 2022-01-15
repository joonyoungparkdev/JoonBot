import discord
from discord.ext import commands
from discord.utils import get

apex_counter = 0  # global variable


class Scanner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, payload: discord.Message):
        if 'apex legends' or 'apex' in payload.content.lower():
            # print("Found!")
            global apex_counter
            apex_counter += 1
            if apex_counter > 1:
                await payload.channel.send(":dog::poop: has been mentioned " + str(apex_counter) + " times")
            else:
                await payload.channel.send(":dog::poop: has been mentioned " + str(apex_counter) + " time")
        # print(payload.content)


def setup(client):
    client.add_cog(Scanner(client))

