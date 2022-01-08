import discord
import os
import json
import requests
import builtins
import random

from discord.ext import commands
from discord.utils import get
from discord import Spotify
from secrets import spotify_token, spotify_user_id


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reaction with a trophy emoji (for fun)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 787119681492090890:
            if payload.emoji.name == "🏆":
                channel = self.client.get_channel(787119681492090890)
                message = await channel.fetch_message(payload.message_id)
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if reaction and reaction.count == 1:
                    await message.channel.send("Let's Go!")
                    # await message.channel.send(f">>Your liked message was: '{message.content}'")
                    # await message.channel.send(f">>Number of times message has been liked: {reaction.count}")
                elif reaction and reaction.count == 2:
                    await message.channel.send("Let's Fucking Go!")
                    # await message.channel.send(f">>Your liked message was: '{message.content}'")
                    # await message.channel.send(f">>Number of times message has been liked: {reaction.count}")
                elif reaction and reaction.count >= 3:
                    await message.channel.send("Too much sauce")
                    # await message.channel.send(f">>Your liked message was: '{message.content}'")
                    # await message.channel.send(f">>Number of times message has been liked: {reaction.count}")

    @commands.command(aliases=['8ball', 'eightball'])
    async def _8ball(self, ctx, *, question="None"):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


def setup(client):
    client.add_cog(Random(client))