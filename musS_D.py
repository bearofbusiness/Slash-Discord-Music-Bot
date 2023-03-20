import asyncio
import discord
import os
import random
from datetime import datetime
from discord.ext import tasks
from dotenv import load_dotenv


# importing other classes from other files
from Queue import Queue
from Song import Song
from YTDLInterface import YTDLInterface

'''
TODO:
    -make more commands
        9- skip (force skip) #sming
        9- pause #bear //vc.pause() and vc.resume()
        9- resume #bear
        9- now #bear
        8- queue #bear
        8- remove #bear
        8- play_top #bear
        8- search #sming
        7- play_list_shuffle #sming
        7- play_list #sming
        6- clear #bear
        5- shuffle #bear
        4- loop (queue, song)
        1- help #bear
        1- volume #nrn
        1- settings (after muliti server) #nrn
        0- filter?(audio effects) #nrn //i dont know if this is possible it may be cool to have tho 
    -other
        6- remove author's songs from queue when author leaves vc #sming
        9- footer that states the progress of the song #bear




DONE:
     - Be able to play music from youtube
        - play music
        - stop music
    (kind but found a better way)- get downloading to work
     - Be able to join vc and play sound
        - join vc
        - leave vc
        - play sound

'''


load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')


class Bot(discord.Client):  # initiates the bots intents and on_ready event
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):

        pront("Bot is ready", lvl="OKGREEN")


# Global Variables
bot = Bot()
tree = discord.app_commands.CommandTree(bot)
queue = Queue()
vc = None


def pront(content, lvl="DEBUG", end="\n") -> None:
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
async def getRandomHex(seed) -> int:
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
async def getEmbed(interaction, title='', content='', footer='', color='') -> discord.Embed:
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
async def send(interaction, title='', content='', footer='', color='', ephemeral: bool = False) -> None:
    embed = await getEmbed(interaction, title, content, footer)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


# Cleans up and closes the player
async def clean(interaction) -> None:
    global vc
    queue.clear()
    player.cancel()
    vc = None
    await interaction.guild.voice_client.disconnect()

# Sends a "Now Playing" embed for a populated Song


async def send_np(song: Song) -> None:
    embed = discord.Embed(
        title='Now Playing:',
        url=song.original_url,
        description=f'{song.title} -- {song.uploader}',
        color=await getRandomHex(song.id)
    )
    embed.add_field(name='Duration:', value=song.parse_duration(
        song.duration), inline=True)
    embed.add_field(name='Requested by:', value=song.requester.mention)
    embed.set_image(url=song.thumbnail)
    embed.set_author(name=song.requester.display_name,
                     icon_url=song.requester.display_avatar.url)
    await song.channel.send(embed=embed)


## COMMANDS ##


@tree.command(name="ping", description="The ping command (^-^)")
async def _ping(interaction: discord.Interaction) -> None:
    # await send(interaction, title='Pong!', content=':ping_pong:')
    await interaction.response.send_message('Pong!', ephemeral=True)


@tree.command(name="join", description="Adds the MaBalls to the voice channel you are in")
async def _join(interaction: discord.Interaction) -> None:
    global vc
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return
    if interaction.guild.voice_client is not None:
        await interaction.response.send_message('I am already in a voice channel', ephemeral=True)
        return
    # Connect to the voice channel
    vc = await interaction.user.voice.channel.connect(self_deaf=True)
    await send(interaction, title='Joined!', content=':white_check_mark:', ephemeral=True)


@tree.command(name="leave", description="Removes the MaBalls from the voice channel you are in")
async def _leave(interaction: discord.Interaction) -> None:
    if interaction.user.voice is None:  # TODO: make it check if the user is in the same voice channel as the bot
        await interaction.response.send_message('You are not in a voice channel with the MaBalls', ephemeral=True)
        return
    if interaction.guild.voice_client is None:
        await interaction.response.send_message('MaBalls is not in a voice channel', ephemeral=True)
        return
    # Disconnect from the voice channel
    await clean(interaction)
    await send(interaction, title='Left!', content=':white_check_mark:', ephemeral=True)


@tree.command(name="play", description="Plays a song from youtube(or other sources somtimes) in the voice channel you are in")
async def _play(interaction: discord.Interaction, link: str) -> None:
    global vc

    # Check if author is in VC
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return

    # If not already in VC, join
    if interaction.guild.voice_client is None:
        channel = interaction.user.voice.channel
        vc = await channel.connect(self_deaf=True)

    song = Song(interaction, link)
    await song.populate()
    # Check if song.populated didnt fail (duration is just a random attribute to check)
    if song.duration is not None:
        queue.add(song)

        embed = discord.Embed(
            title='Added to Queue:',
            url=song.original_url,
            color=await getRandomHex(song.id)
        )
        embed.add_field(name=song.uploader, value=song.title)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.set_thumbnail(url=song.thumbnail)
        embed.set_author(name=song.requester.display_name,
                         icon_url=song.requester.display_avatar.url)
        await interaction.response.send_message(embed=embed)

        # If the player isn't already running, start it.
        if not player.is_running():
            player.start()
    else:
        await send(interaction, title='Error!', content='Invalid link', ephemeral=True)


@tasks.loop()
async def player() -> None:
    global vc
    while True:
        # Pull the top song in queue
        song = queue.remove(0)
        await song.populate()
        # There should be ~10 seconds left before the current song is over, wait it out.
        while vc.is_playing():
            await asyncio.sleep(1)

        await send_np(song)
        vc.play(discord.FFmpegPCMAudio(
            song.audio, **YTDLInterface.ffmpeg_options))
        # Wait until 10 seconds before the song ends to queue up the next one.
        await asyncio.sleep(song.duration - 10)
        # If we see the queue is empty, get ready to close
        if not queue.get():
            # Keep checking for those last 10 seconds
            while vc.is_playing():
                await asyncio.sleep(0.5)
                # If a song is added in this time, abort early to let us get ready for it.
                if queue.get():
                    return  # returns to the first loop
            # Kill the player and leave VC
            break
    player.stop()
    await song.channel.guild.voice_client.disconnect()
bot.run(key)
