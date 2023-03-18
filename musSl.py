import interactions
import discord
from discord.ext import commands
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

'''
TODO:
     -get downloading to work
        -get it to download to disk
        -get to download to memory
     - Be able to join vc and play sound
        - join vc
        - leave vc
        - play sound
     - Be able to play music from youtube
        - play music
        - stop music
'''


load_dotenv()
key = os.environ.get('key')


bot = interactions.Client(token=key)


def pront(content, lvl="DEBUG"):
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
    print(colors[lvl] + "{" + datetime.now().strftime("%x %X") +
          "} " + lvl + ": " + str(content) + colors["NONE"])


async def getRandomHex(seed=None):
    random.seed(int(seed))
    return random.randint(0, 16777215)


async def getEmbed(ctx, title='', content='', footer='', color=''):
    if color == '':
        color = await getRandomHex(seed=ctx.author.id)

    embed = interactions.Embed(
        title=title,
        description=content,
        color=color
    )
    embed.set_author(name=ctx.author.name  # ,
                     , icon_url="https://bearofbusines.me/gorilla.png")
    embed.set_footer(text=footer)
    # dir(embed)
    return embed


async def send(ctx, title='', content='', footer='', color='', time=1800):
    embed = await getEmbed(ctx, title, content, footer)
    await ctx.send(embeds=embed)  # , delete_after=time


@ bot.command(
    name="test_command",
    description="This is the test command",
)
async def test_command(ctx: interactions.CommandContext):
    # message = await ctx.send('Sometext')
    await send(ctx, title="Hello World!", footer="MaBalls")


@commands.is_owner()
@bot.command(
    name="execute",
    description="This is the exec command only can be used be owner for obvious reasons",
    options=[
        interactions.Option(
            name="input",
            description="The input to be executed",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def execute(ctx, input: str):
    if (ctx.author.id == 369999044023549962):
        comand = input
        pront(comand, "LOG")
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        comand = comand.rstrip('`')
        comand = comand.lstrip('`')
        comand = comand.lstrip('python')
        # pront(comand)

        try:
            exec(comand)
        except Exception as e:
            pront(e, "ERROR")
        sys.stdout = old_stdout
        # pront("LOG", mystdout.getvalue())
        print(mystdout.getvalue())
        await send(ctx, title='Command Sent:', content='in:\n```python\n' + comand + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```', footer='MABALLS')
    else:
        await send(ctx, title='You Do Not Have Perms', footer='MABALLS')


bot.start()
