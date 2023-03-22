import discord
import os
import random
import math
import time
from datetime import datetime
from dotenv import load_dotenv

# importing other classes from other files
from Song import Song
from Servers import Servers
from Player import Player

# needed to add it to a var bc of pylint on my laptop but i delete it right after
XX = '''
#-fnt stands for finished not tested
#-f is just finished
TODO:
    -make more commands
        9-fnt skip (force skip) #sming
        8- search #sming
        7- play_list_shuffle #sming
        7- play_list #sming
        7- remove user's songs from queue
        1- help #bear
        1- volume #nrn
        1- settings #nrn //after muliti server
    -other
        6- remove author's songs from queue when author leaves vc #sming




DONE:
     - make more commands
        9-f pause #bear //vc.pause() and vc.resume()
        9-f resume #bear
        9-f now #bear
        8-f queue #bear
        8-f remove #bear
        8-f play_top #bear
        6-f clear #bear
        5-f shuffle #bear
        4-f loop (queue, song) #bear
     - Be able to play music from youtube
        - play music
        - stop music
    (kind but found a better way)- get downloading to work
     - Be able to join vc and play sound
        - join vc
        - leave vc
        - play sound
    - other
        9-f footer that states the progress of the song #bear
        3- make it multi server #bear

'''
del XX

load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')


class Bot(discord.Client):  # initiates the bots intents and on_ready event
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        await tree.sync()  # please dont remove just in case i need to sync
        pront("Bot is ready", lvl="OKGREEN")


# Global Variables
bot = Bot()
tree = discord.app_commands.CommandTree(bot)
servers = Servers()


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
async def get_progress_bar(song: Song) -> str:
    # if the song is None or the song has been has not been started (-100 is an arbitrary number)
    if song is None or await song.get_elapsed_time() > time.time() - 1000 or servers.get_player(song.channel.guild.id).vc.is_playing() is False:
        return ''
    percent_duration = (await song.get_elapsed_time() / song.duration)*100
    ret = f'{song.parse_duration_short_hand(math.floor(await song.get_elapsed_time()))}/{song.parse_duration_short_hand(song.duration)}'
    ret += f' [{(math.floor(percent_duration / 4) * "▬")}{">" if percent_duration < 100 else ""}{((math.floor((100 - percent_duration) / 4)) * "    ")}]'
    print(ret)
    return ret


# Returns a random hex code
def get_random_hex(seed) -> int:
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
async def get_embed(interaction, title='', content='', url=None, color='', progress: bool = True) -> discord.Embed:
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
        player = servers.get_player(interaction.guild_id)
        footer_message = f'{":repeat: " if player.looping else ""}{":repeat_one: " if player.queue_looping else ""}\n{await get_progress_bar(player.queue.get(0))}'

        embed.set_footer(text=footer_message,
                         icon_url=player.queue.get(0).thumbnail)
    return embed


# Creates and sends an Embed message
async def send(interaction: discord.Interaction, title='', content='', url='', color='', ephemeral: bool = False, progress: bool = True) -> None:
    embed = await get_embed(interaction, title, content, url, color, progress)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


# Cleans up and closes the player
async def clean(id: int) -> None:
    await servers.get_player(id).vc.disconnect()
    servers.get_player(id).terminate_player()
    servers.remove(id)


## COMMANDS ##


@ tree.command(name="ping", description="The ping command (^-^)")
async def _ping(interaction: discord.Interaction) -> None:
    # await send(interaction, title='Pong!', content=':ping_pong:')
    await interaction.response.send_message('Pong!', ephemeral=True)


@ tree.command(name="join", description="Adds the MaBalls to the voice channel you are in")
async def _join(interaction: discord.Interaction) -> None:
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return
    if interaction.guild.voice_client is not None:
        await interaction.response.send_message('I am already in a voice channel', ephemeral=True)
        return
    # Connect to the voice channel
    vc = await interaction.user.voice.channel.connect(self_deaf=True)
    servers.add(interaction.guild_id, Player(vc))
    await send(interaction, title='Joined!', content=':white_check_mark:', ephemeral=True)


@ tree.command(name="leave", description="Removes the MaBalls from the voice channel you are in")
async def _leave(interaction: discord.Interaction) -> None:
    if interaction.guild.voice_client is None:
        await interaction.response.send_message('MaBalls is not in a voice channel', ephemeral=True)
        return
    if interaction.user.voice is None or interaction.user.voice.channel != interaction.guild.voice_client.channel:
        await interaction.response.send_message('You are not in a voice channel with the MaBalls', ephemeral=True)
        return

    # Disconnect from the voice channel
    await clean(interaction.guild_id)
    await send(interaction, title='Left!', content=':white_check_mark:', ephemeral=True)


@ tree.command(name="play", description="Plays a song from youtube(or other sources somtimes) in the voice channel you are in")
async def _play(interaction: discord.Interaction, link: str) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)
    # Check if author is in VC
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return

    # If not already in VC, join
    if interaction.guild.voice_client is None:
        channel = interaction.user.voice.channel
        vc = await channel.connect(self_deaf=True)
        servers.add(interaction.guild_id, Player(vc))

    song = Song(interaction, link)
    await song.populate()
    # Check if song.populated didnt fail (duration is just a random attribute to check)
    if song.duration is not None:
        servers.get_player(interaction.guild_id).queue.add(song)
        embed = await get_embed(
            interaction,
            title='Added to Queue:',
            url=song.original_url,
            color=get_random_hex(song.id)
        )
        embed.add_field(name=song.uploader, value=song.title)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.set_thumbnail(url=song.thumbnail)
        await interaction.followup.send(embed=embed)
        # If the player isn't already running, start it.
        if not servers.get_player(interaction.guild_id).is_started():
            await servers.get_player(interaction.guild_id).start()
    else:
        await interaction.followup.send(await get_embed(interaction, title='Error!', content='Invalid link', progress=False), ephemeral=True)


@ tree.command(name="skip", description="Skips the currently playing song")
async def _skip(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    # Get a complex embed for votes

    async def skip_msg(title='', content='', present_tense=True, ephemeral=False):
        current_song = servers.get_player(
            interaction.guild_id).queue.get(0)
        embed = await get_embed(interaction, title, content, color=get_random_hex(current_song.id))
        if present_tense:
            song_message = "Song being voted on:"
        else:
            song_message = "Song that was voted on:"
        embed.add_field(name=song_message,
                        value=current_song.title, inline=True)
        embed.set_thumbnail(url=current_song.thumbnail)
        users = ''
        embed.add_field(name="Initiated by:", value=servers.get_skip_vote(
            interaction.guild_id).initiator)
        for user in servers.get_player(interaction.guild_id).song.vote.get():
            users = f'{user.name}, {users}'
        users = users[:-2]
        if present_tense:
            # != 1 because if for whatever reason len(skip_vote) == 0 it will still make sense
            voter_message = f"User{'s who have' if len(servers.get_player(interaction.guild_id).song.vote) != 1 else ' who has'} voted to skip:"
        else:
            voter_message = f"Vote passed by:"
        embed.add_field(name=voter_message, value=users, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    # If there's enough people for it to make sense to call a vote in the first place
    # TODO SET THIS BACK TO 3, SET TO 1 FOR TESTING
    if len(servers.get_player(interaction.guild_id).vc.channel.members) > 1:
        votes_required = len(servers.get_player(
            interaction.guild_id).vc.channel.members) // 2

        if servers.get_player(interaction.guild_id).song.vote is None:
            # Create new Vote
            servers.get_player(interaction.guild_id).song.create_vote(
                interaction.user)
            await skip_msg("Vote added.", f"{votes_required - len(servers.get_player(interaction.guild_id).song.vote)}/{votes_required} votes to skip.")
            return

        # If user has already voted to skip
        if interaction.user in servers.get_player(interaction.guild_id).song.vote.get():
            await skip_msg("You have already voted to skip!", ":octagonal_sign:", ephemeral=True)
            return

        # Add vote
        servers.get_skip_vote(
            interaction.guild_id).add(interaction.user)

        # If vote succeeds
        if len(servers.get_player(interaction.guild_id).song.vote) >= votes_required:
            await skip_msg("Skip vote succeeded! :tada:", present_tense=False)
            # Kill and restart the player to queue the next song.
            servers.get_player(interaction.guild_id).terminate_player()
            servers.get_player(interaction.guild_id).vc.stop()
            await servers.get_player(interaction.guild_id).start()
            servers.get_player(interaction.guild_id).song.vote, = None
            if not servers.get_player(interaction.guild_id).queue.get():
                await clean()
            return

        await skip_msg("Vote added.", f"{votes_required - len(servers.get_player(interaction.guild_id).song.vote)}/{votes_required} votes to skip.")
    # If there isn't just skip
    else:
        await _force_skip(interaction)


@ tree.command(name="force_skip", description="Skips the currently playing song without having a vote.")
async def _force_skip(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    # Kill and restart the player to queue the next song.
    servers.get_player(interaction.guild_id).terminate_player()
    servers.get_player(interaction.guild_id).vc.stop()
    await servers.get_player(interaction.guild_id).start()
    if not servers.get_player(interaction.guild_id).queue.get():
        await clean()
    await send(interaction, "Skipped!", ":white_check_mark:")


@ tree.command(name="queue", description="Shows the current queue")
async def _queue(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    if not servers.get_player(interaction.guild_id).queue.get():
        await send(interaction, title='Queue is empty!', ephemeral=True)
        return
    embed = await get_embed(interaction, title='Queue', color=get_random_hex(servers.get_player(interaction.guild_id).queue.get()[0].id), progress=False)
    for i, song in enumerate(servers.get_player(interaction.guild_id).queue.get()):
        embed.add_field(name=song.title,
                        value=f"{i}. by {song.uploader}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@ tree.command(name="now", description="Shows the current song")
async def _now(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    player = servers.get_player(interaction.guild_id)
    title_message = f'Now Playing:\t{":repeat: " if player.looping else ""}{":repeat_one: " if player.queue_looping else ""}'
    embed = await get_embed(interaction,
                            title=title_message,
                            url=player.song.original_url,
                            content=f'{player.song.title} -- {player.song.uploader}',
                            color=get_random_hex(
                                player.song.id)
                            )
    embed.add_field(name='Duration:', value=player.song.parse_duration(
        player.song.duration), inline=True)
    embed.add_field(name='Requested by:', value=player.song.requester.mention)
    embed.set_image(url=player.song.thumbnail)
    embed.set_author(name=player.song.requester.display_name,
                     icon_url=player.song.requester.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@ tree.command(name="remove", description="Removes a song from the queue")
async def _remove(interaction: discord.Interaction, number_in_queue: int) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    removed_song = servers.get_player(
        interaction.guild_id).queue.remove(number_in_queue + 1)
    if removed_song is not None:
        embed = discord.Embed(
            title='Removed from Queue:',
            url=removed_song.original_url,
            color=get_random_hex(removed_song.id)
        )
        embed.add_field(name=removed_song.uploader, value=removed_song.title)
        embed.add_field(name='Requested by:',
                        value=removed_song.requester.mention)
        embed.set_thumbnail(url=removed_song.thumbnail)
        embed.set_author(name=removed_song.requester.display_name,
                         icon_url=removed_song.requester.display_avatar.url)
        await interaction.response.send_message(embed=embed)


@ tree.command(name="play_top", description="Plays a song from youtube(or other sources somtimes) in the voice channel you are in")
async def _play_top(interaction: discord.Interaction, link: str) -> None:

    # Check if author is in VC
    if interaction.user.voice is None:
        await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
        return

    # If not already in VC, join
    if interaction.guild.voice_client is None:
        channel = interaction.user.voice.channel
        vc = await channel.connect(self_deaf=True)
        servers.add(interaction.guild_id, Player(vc))

    song = Song(interaction, link)
    await song.populate()
    # Check if song.populated didnt fail (duration is just a random attribute to check)
    if song.duration is not None:
        servers.get_player(interaction.guild_id).queue.add_at(song, 1)

        embed = await get_embed(interaction,
                                title='Added to the top of the Queue:',
                                url=song.original_url,
                                color=get_random_hex(song.id)
                                )
        embed.add_field(name=song.uploader, value=song.title)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.set_thumbnail(url=song.thumbnail)
        await interaction.response.send_message(embed=embed)

        # If the player isn't already running, start it.
        if not servers.get_player(interaction.guild_id).is_started():
            await servers.get_player(interaction.guild_id).start()
    else:
        await send(interaction, title='Error!', content='Invalid link', ephemeral=True)


@ tree.command(name="clear", description="Clears the queue")
async def _clear(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    servers.get_player(interaction.guild_id).queue.clear()
    await interaction.response.send_message('Queue cleared')


@ tree.command(name="shuffle", description="Shuffles the queue")
async def _shuffle(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    servers.get_player(interaction.guild_id).queue.shuffle()
    await interaction.response.send_message('Queue shuffled')


@ tree.command(name="pause", description="Pauses the current song")
async def _pause(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    servers.get_player(interaction.guild_id).vc.pause()
    await servers.get_player(interaction.guild_id).song.pause()
    await send(interaction, title='Paused')


@ tree.command(name="resume", description="Resumes the current song")
async def _resume(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    servers.get_player(interaction.guild_id).vc.resume()
    await servers.get_player(interaction.guild_id).song.resume()
    await send(interaction, title='Resumed')


@ tree.command(name="loop", description="Loops the current song")
async def _loop(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    player = servers.get_player(interaction.guild.id)
    player.set_loop(not player.looping)
    await send(interaction, title='Looped.' if player.looping else 'Loop disabled.')


@ tree.command(name="queue_loop", description="Loops the queue")
async def _queue_loop(interaction: discord.Interaction) -> None:
    if servers.get_player(interaction.guild.id) == None:
        await send(interaction, title='Error!', content='Not in vc', ephemeral=True)
        return
    player = servers.get_player(interaction.guild.id)
    player.set_queue_loop(not player.queue_looping)
    await send(interaction, title='Queue looped.' if player.queue_looping else 'Queue loop disabled.')


bot.run(key)
