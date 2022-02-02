import discord
from discord.ext import commands
from discord.utils import get

scanlist = ['apex legends', 'apexlegends', 'apex']
valorant_role = 'Radiants'


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
                # print(apex_data)
                counter = int(apex_data.content) + 1     # add one to the count and store as new var
                await apex_data.edit(content=str(counter))
                # print(scanlist)

                if counter > 1:
                    await payload.channel.send(":dog::poop: has been mentioned " + str(counter) + " times")
                else:
                    await payload.channel.send(":dog::poop: has been mentioned " + str(counter) + " time")
            # print(payload.content)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        valorant_voice = self.client.get_channel(936645156726276186)
        general_chat = self.client.get_channel(790748856290639882)
        guild = self.client.get_guild(786639331930275910)
        users = self.client.get_all_members()
        testroom = self.client.get_channel(787119681492090890)
        if after.channel == valorant_voice:

            for role in valorant_voice.guild.roles:     # loop thru all roles in server
                if str(role) == valorant_role:          # if role is desired role
                    for user in role.members:           # loop thru all role members
                        # print(">" + str(user))
                        # print(user.voice)
                        if user.voice is None:   # if member is not already in voice
                            # print(user)
                            channel = await user.create_dm()
                            await channel.send('Tryna run some Valorant? <#936645156726276186> ~ ' + str(member))

            # channel = await member.create_dm()
            # await channel.send('dmd')


def setup(client):
    client.add_cog(Scanner(client))
