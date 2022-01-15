import discord
from discord.ext import commands
from discord.utils import get

scanlist = ['apex legends', 'apex']


class Scanner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, payload: discord.Message):
        for x in scanlist:
            if x in payload.content.lower():
                # print("Found!")
                data_channel = self.client.get_channel(932013482486947951)

                # await data_channel.send("**__Apex Counter:__**")
                # await data_channel.send("0")

                apex_data = await data_channel.fetch_message(932024492295872522)
                print(apex_data.content)
                counter = int(apex_data.content) + 1     # add one to the count and store as new var
                await apex_data.edit(content=str(counter))
                # print(scanlist)

                if counter > 1:
                    await payload.channel.send(":dog::poop: has been mentioned " + str(counter) + " times")
                else:
                    await payload.channel.send(":dog::poop: has been mentioned " + str(counter) + " time")
            # print(payload.content)


def setup(client):
    client.add_cog(Scanner(client))

