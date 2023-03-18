import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import functools
from io import StringIO
import itertools
import math
import random
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

import json
from yt_dlp import YoutubeDL


load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')


def pront(content, lvl="DEBUG", end="\n"):
    colors = {
        "LOG": "",
        "DEBUG": "\033[1;95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "NONE": "\033[0m"
    }
    # if type(content) != str and type(content) != int and type(content) != float:
    #    content = sep.join(content)
    print(colors[lvl] + "{" + datetime.now().strftime("%x %X") +
          "} " + lvl + ": " + str(content) + colors["NONE"], end=end)  # sep.join(list())


# Returns a random hex code
async def getRandomHex(seed):
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
async def getEmbed(interaction, title='', content='', footer='', color=''):
    if color == '':
        color = await getRandomHex(interaction.user.id)
    embed = discord.Embed(
        title=title,
        description=content,
        color=color
    )
    embed.set_author(name=interaction.user.display_name,
                     icon_url=interaction.user.display_avatar.url)
    # TODO Hide the footer until i find out what to do with it
    # embed.set_footer(footer=footer)
    return embed


# Creates and sends an Embed message
async def send(interaction, title='', content='', footer='', color='', ephemeral: bool=False):
    embed = await getEmbed(interaction, title, content, footer)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents(value=3467840))
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        pront("Bot is ready", lvl="OKGREEN")


bot = Bot()
tree = app_commands.CommandTree(bot)


@tree.command(name="ping", description="The ping command")
async def _ping(interaction: discord.Interaction):
    pront(dir(interaction), end="\n\n")
    pront(dir(interaction.channel), end="\n\n")
    pront(dir(interaction.client), end="\n\n")
    pront(dir(interaction.user), end="\n\n")
    # await send(interaction, title='Pong!', content=':ping_pong:')
    await interaction.response.send_message('Pong!', ephemeral=True)


bot.run(key)  # make sure you set your intents in the portal and here on line 10


'''
@bot.command(aliases=['eval'])
# @tree.command(name="commandname", description="My first application Command")
# @bot.tree.command(name="eval", description="The eval command",)
@commands.is_owner()
async def _eval(ctx: discord.Interaction, comand=None):
    # if (ctx.author.id == {idhere}):#for when you are not owner but want to make it so only you can use it
    # pront("LOG", comand)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    comand.rstrip("`")
    comand.lstrip("`")
    comand.lstrip("python")
    try:
        print(eval(comand))
    except Exception as e:
        pront(e, "ERROR")
    sys.stdout = old_stdout
    # pront("LOG", mystdout.getvalue())
    print(mystdout.getvalue())
    await send(ctx, title='Command Sent:', content='in:\n```' + comand + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')
#    else:#sends no perms if has none
#        await send(ctx, title='You Do Not Have Perms')


@bot.command(aliases=['exec'])
@commands.is_owner()
async def _exec(ctx, *, comand=None):
    # if (ctx.author.id == {idhere}):#for when you are not owner 369999044023549962
    # pront("LOG", comand)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    comand = comand.rstrip("`")
    comand = comand.lstrip("`")
    comand = comand.lstrip("python")
    # pront(comand)

    try:
        exec(comand)
    except Exception as e:
        pront(e, "ERROR")
    sys.stdout = old_stdout
    # pront("LOG", mystdout.getvalue())
    print(mystdout.getvalue())
    await send(ctx, title='Command Sent:', content='in:\n```' + comand + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')
#    else:#sends no perms if has none
#        await send(ctx, title='You Do Not Have Perms')
'''
