# Joon Bot

import os

import discord
from discord.ext import commands
from secrets import discord_token

client = commands.Bot(command_prefix='!', case_insensitive=True)

DISCORD_TOKEN = discord_token
# DISCORD_TOKEN = os.environ['DISCORD_TOKEN']


@client.event
async def on_ready():
    print('Bot is Ready')
    await client.change_presence(activity=discord.Game('With Mommy Milkers'))


# ex: '.load example'
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been loaded!')


# ex: '.unload example'
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been unloaded!')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been reloaded!')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(DISCORD_TOKEN)
