import discord
import math
import random
import time

from datetime import datetime

# Import classes from our files
from Player import Player
from Servers import Servers
from Song import Song

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


# makes a ascii song progress bar
def get_progress_bar(song: Song) -> str:
    # if the song is None or the song has been has not been started ( - 100000 is an arbitrary number)
    if song is None or song.get_elapsed_time() > time.time() - 100000:
        return ''
    percent_duration = (song.get_elapsed_time() / song.duration)*100
    ret = f'{song.parse_duration_short_hand(math.floor(song.get_elapsed_time()))}/{song.parse_duration_short_hand(song.duration)}'
    ret += f' [{(math.floor(percent_duration / 4) * "▬")}{">" if percent_duration < 100 else ""}{((math.floor((100 - percent_duration) / 4)) * "    ")}]'
    return ret


# Returns a random hex code
def get_random_hex(seed) -> int:
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
def get_embed(interaction, title='', content='', url=None, color='', progress: bool = True) -> discord.Embed:
    if color == '':
        color = get_random_hex(interaction.user.id)
    embed = discord.Embed(
        title=title,
        description=content,
        url=url,
        color=color
    )
    embed.set_author(name=interaction.user.display_name,
                     icon_url=interaction.user.display_avatar.url)

    # If the calling method wants the progress bar
    if progress:
        player = Servers.get_player(interaction.guild_id)
        if player is not None and player.is_started() and player.queue.get():
            footer_message = f'{"🔁 " if player.looping else ""}{"🔂 " if player.queue_looping else ""}\n{get_progress_bar(player.queue.top())}'

            embed.set_footer(text=footer_message,
                             icon_url=player.queue.top().thumbnail)
    return embed


# Creates and sends an Embed message
async def send(interaction: discord.Interaction, title='', content='', url='', color='', ephemeral: bool = False, progress: bool = True) -> None:
    embed = get_embed(interaction, title, content, url, color, progress)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

def get_now_playing_embed(player: Player, progress: bool=False) -> discord.Embed:
        title_message = f'Now Playing:\t{":repeat: " if player.looping else ""}{":repeat_one: " if player.queue_looping else ""}'
        embed = discord.Embed(
            title=title_message,
            url=player.song.original_url,
            description=f'{player.song.title} -- {player.song.uploader}',
            color=get_random_hex(player.song.id)
        )
        embed.add_field(name='Duration:', value=player.song.parse_duration(
            player.song.duration), inline=True)
        embed.add_field(name='Requested by:', value=player.song.requester.mention)
        embed.set_image(url=player.song.thumbnail)
        embed.set_author(name=player.song.requester.display_name,
                         icon_url=player.song.requester.display_avatar.url)
        if progress:
            embed.set_footer(text=get_progress_bar(player.song))
        return embed


# Cleans up and closes a player
async def clean(player: Player) -> None:
    player.terminate_player()
    # Delete a to-be defunct now_playing message
    if player.last_np_message:
        await player.last_np_message.delete()
    player.queue.clear()
    await player.vc.disconnect()
    Servers.remove(id)


# Runs various tests to make sure a command is OK to run
async def pretests(interaction: discord.Interaction) -> bool:
    if interaction.guild.voice_client is None:
        await interaction.response.send_message("MaBalls is not in a voice channel", ephemeral=True)
        return False

    if interaction.user.voice.channel != interaction.guild.voice_client.channel:
        await interaction.response.send_message("You must be connected to the same voice channel as MaBalls", ephemeral=True)
        return False
    return True


async def ext_pretests(interaction: discord.Interaction) -> bool:
    if not await pretests(interaction):
        return False
    # TODO This does not actually check if audio is playing at this exact moment, things can still be populating
    if not Servers.get_player(interaction.guild_id).is_started():
        await interaction.response.send_message("This command can only be used while a song is playing", ephemeral=True)
        return False

    return True


async def join_pretests(interaction: discord.Integration) -> bool:
    # Check if author is in VC
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return False
    # Exception to pretests() because it will join a voice channel

    # If not already in VC, join
    if interaction.guild.voice_client is None:
        channel = interaction.user.voice.channel
        vc = await channel.connect(self_deaf=True)
        Servers.add(interaction.guild_id, Player(vc))
    # Otherwise, make sure the user is in the same channel
    elif interaction.user.voice.channel != interaction.guild.voice_client.channel:
        await interaction.response.send_message("You must be in the same voice channel in order to use MaBalls", ephemeral=True)
        return False
    return True