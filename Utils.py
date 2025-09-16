import asyncio
import discord
import math
import random
import time
import yt_dlp.utils

from datetime import datetime

# Import classes from our files
from Player import Player
from Servers import Servers
from Song import Song

asyncio_tasks = set()


async def respond(ctx, *args, **kwargs) -> None:
    """Send a response to a provided context or interaction.

    This helper normalizes responding between :class:`discord.ApplicationContext`,
    :class:`discord.Interaction`, and :class:`discord.ext.commands.Context` objects.
    It will automatically fall back to followup messages when the initial
    response has already been used and gracefully ignore unsupported keyword
    arguments such as ``ephemeral`` when sending to regular text channels.

    Parameters
    ----------
    ctx: ``discord.ApplicationContext`` | ``discord.Interaction`` | ``discord.ext.commands.Context``
        The context or interaction to respond to.
    *args:
        Positional arguments forwarded to the respective send method.
    **kwargs:
        Keyword arguments forwarded to the respective send method.
    """

    ephemeral = kwargs.get("ephemeral")

    if hasattr(ctx, "respond"):
        try:
            await ctx.respond(*args, **kwargs)
        except discord.InteractionResponded:
            followup = getattr(ctx, "followup", None)
            if followup is None:
                raise
            followup_kwargs = kwargs.copy()
            await followup.send(*args, **followup_kwargs)
        return

    response = getattr(ctx, "response", None)
    if response is not None:
        is_done = getattr(response, "is_done", None)
        if callable(is_done) and is_done():
            followup = getattr(ctx, "followup", None)
            if followup is not None:
                await followup.send(*args, **kwargs)
                return
        await response.send_message(*args, **kwargs)
        return

    send_method = getattr(ctx, "send", None)
    if callable(send_method):
        send_kwargs = kwargs.copy()
        if ephemeral is not None:
            send_kwargs.pop("ephemeral", None)
        await send_method(*args, **send_kwargs)
        return

    interaction = getattr(ctx, "interaction", None)
    if interaction is not None and interaction is not ctx:
        await respond(interaction, *args, **kwargs)
        return

    raise TypeError("Provided context does not support sending a response.")

def pront(content, lvl="DEBUG", end="\n") -> None:
    """
    A custom logging method that acts as a wrapper for print().

    Parameters
    ----------
    content : `any`
        The value to print.
    lvl : `str`, optional
        The level to raise the value at.
        Accepted values and their respective colors are as follows:

        LOG : None
        DEBUG : Pink
        OKBLUE : Blue
        OKCYAN : Cyan
        OKGREEN : Green
        WARNING : Yellow
        ERROR : Red
        NONE : Resets ANSI color sequences
    end : `str` = `\\n` (optional)
        The character(s) to end the statement with, passes to print().
    """
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
    """
    Creates an ASCII progress bar from a provided Song.
    
    This is calculated from a time delta counted within the song.

    Parameters
    ----------
    song : `Song`
        The Song object to create the progress bar from.
    
    Returns
    -------
    `str`:
        A string containing a visual representation of how far the song has played.
    """
    # if the song is None or the song has been has not been started ( - 100000 is an arbitrary number)
    if song is None or song.get_elapsed_time() > time.time() - 100000 or song.duration is None:
        return ''
    percent_duration = (song.get_elapsed_time() / song.duration)*100

    if percent_duration > 100:#percent duration cant be greater than 100
        return 'The player has stalled, please run /force-reset-player.'

    ret = f'{song.parse_duration_short_hand(math.floor(song.get_elapsed_time()))}/{song.parse_duration_short_hand(song.duration)}'
    ret += f' [{(math.floor(percent_duration / 4) * "▬")}{">" if percent_duration < 100 else ""}{((math.floor((100 - percent_duration) / 4)) * " ")}]'
    return ret

@DeprecationWarning
def progress_bar(begin: int, end: int, current_val: int) -> str:
    """
    A deprecated method for producing progress bars that only requires integers
    """
    percent_duration = (current_val / end) * 100

    if percent_duration > 100:#percent duration cant be greater than 100
        percent_duration = 100

    ret = f'{current_val}/{end}'
    ret += f' [{(math.floor(percent_duration / 4) * "▬")}{">" if percent_duration < 100 else ""}{((math.floor((100 - percent_duration) / 4)) * "    ")}]'
    return ret

# Returns a random hex code
def get_random_hex(seed = None) -> int:
    """
    Returns a random hexidecimal color code.
    
    Parameters
    ----------
    seed : `int` | `float` | `str` | `bytes` | `bytearray` (optional)
        The seed to generate the color from.
        None or no argument seeds from current time or from an operating system specific randomness source if available.

    Returns
    -------
    `int`:
        The integer representing the hexidecimal code.
    """
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
def get_embed(ctx, title='', content='', url=None, color='', progress: bool = True) -> discord.Embed:
    """
    Quick and easy method to create a discord.Embed that allows for easier keeping of a consistent style

    TODO change the content parameter to be named description to allow it to align easier with the standard discord.Embed() constructor.

    Parameters
    ----------
    ctx : `discord.ApplicationContext` | `discord.Interaction` | `commands.Context`
        The context or interaction to draw author information from.
    title : `str` (optional)
        The title of the embed. Can only be up to 256 characters.
    content : `str` (optional)
        The description of the embed. Can only be up to 4096 characters.
    url : `str` | `None` (optional)
        The URL of the embed.
    color : `int` (optional)
        The color of the embed.
    progress : `bool` = `True` (optional)
        Whether get_embed should try to automatically add the progress bar and now-playing information.

    Returns
    -------
    `discord.Embed`:
        The embed generated by the parameters.
    """
    ctx_user = getattr(ctx, "user", None) or getattr(ctx, "author", None)
    if ctx_user is None:
        raise AttributeError("Provided context is missing user information required for embeds.")

    if color == '':
        color = get_random_hex(getattr(ctx_user, "id", None))
    embed = discord.Embed(
        title=title,
        description=content,
        url=url,
        color=color
    )
    display_name = getattr(ctx_user, "display_name", str(ctx_user))
    avatar = getattr(getattr(ctx_user, "display_avatar", None), "url", None)
    embed.set_author(name=display_name, icon_url=avatar)

    # If the calling method wants the status bar
    if progress:
        guild_id = getattr(ctx, "guild_id", None)
        if guild_id is None:
            guild = getattr(ctx, "guild", None)
            if guild is not None:
                guild_id = guild.id
        if guild_id is not None:
            player = Servers.get_player(guild_id)
        else:
            player = None
        if player and player.is_playing():

            embed.set_footer(text= f'{"🔂 " if player.looping else ""}{"🔁 " if player.queue_looping else ""}{"♾ " if player.true_looping else ""}',
                             icon_url=player.song.thumbnail)
    return embed


# Creates and sends an Embed message
async def send(ctx: discord.ApplicationContext, title='', content='', url='', color='', ephemeral: bool = False, progress: bool = True) -> None:
    """
    A convenient method to send a get_embed generated by its parameters.

    Parameters
    ----------
    ctx : `discord.ApplicationContext` | `discord.Interaction` | `commands.Context`
        The context or interaction to draw author information from.
    title : `str` (optional)
        The title of the embed. Can only be up to 256 characters.
    content : `str` (optional)
        The description of the embed. Can only be up to 4096 characters.
    url : `str` | `None` (optional)
        The URL of the embed.
    color : `int` (optional)
        The color of the embed.
    progress : `bool` = `True` (optional)
        Whether get_embed should try to automatically add the progress bar and now-playing information.
    ephemeral : `bool` = `False` (optional)
    """
    embed = get_embed(ctx, title, content, url, color, progress)
    await respond(ctx, embed=embed, ephemeral=ephemeral)


def get_now_playing_embed(player: Player, progress: bool = False) -> discord.Embed:
    """
    Gets an embed for a now-playing messge.
    Used for consistency and neatness.

    Parameters
    ----------
    player : `Player`
        The player to gather states, etc. from.
    progress : `bool`, `False`, optional
        Whether the embed should generate with a progress bar.

    Returns
    -------
    `discord.Embed`:
        The now-playing embed.

    """
    # If the player isn't currently playing something
    if not player.is_playing():
        return discord.Embed(title='Nothing is playing.')
    title_message = f'Now Playing:\t{":repeat_one: " if player.looping else ""}{":repeat: " if player.queue_looping else ""}{":infinity: " if player.true_looping else ""}'
    embed = discord.Embed(
        title=title_message,
        url=player.song.original_url,
        description=f'{player.song.title} -- {player.song.uploader}',
        color=get_random_hex(player.song.id)
    )
    embed.add_field(name='Duration:', value=player.song.parse_duration(
        player.song.duration), inline=True)
    embed.add_field(name='Requested by:', value=player.song.requester.mention)
    if progress:
        embed.add_field(name='Timestamp:', value=f"`{get_progress_bar(player.song)}`", inline=False)
    embed.set_image(url=player.song.thumbnail)
    embed.set_author(name=player.song.requester.display_name,
                     icon_url=player.song.requester.display_avatar.url)
    
    return embed

def populate_song_list(songs: list[Song], guild_id: int) -> None:
    """
    Creates a task to populate a list of songs in parallel.
    Is cognizant of a player and will halt itself in the event of its expiry.
    
    Parameters
    ----------
    songs : `list[Song]`
        The list of songs to iterate over.
    guild_id : `int`
        The id of the guild that the player to watch belongs to.
    """

    async def __primary_loop(songs: list[Song], guild_id: int) -> None:
        """
        Iterates over a list of Songs and populates them while checking if the Player they belong to still exists.
        
        Parameters
        ----------
        songs : `list[Song]`
            The list of songs to iterate over.
        guild_id : `int`
            The id of the guild that the player to watch belongs to.
        """
        for i in range(len(songs)):
            if Servers.get_player(guild_id) is None:
                return
            pront(f"populating {songs[i].title}")
            try:
                await songs[i].populate()
            except yt_dlp.utils.ExtractorError:
                pront('raised ExtractorError', 'ERROR')
            except yt_dlp.utils.DownloadError:
                pront('raised DownloadError', 'ERROR')
            songs[i] = None

    task = asyncio.create_task(__primary_loop(songs, guild_id))
    asyncio_tasks.add(task)
    task.add_done_callback(asyncio_tasks.discard)

async def force_reset_player(player: Player) -> None:
    """Forcibly restarts a player without losing any of the queue information contained within.
    
    Parameters
    ----------
    player : `Player`
        The player to restart.
    """
    await player.clean()
    plaer.guild.change_voice_state()
    await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
    player.vc.voice_connect()
    player.vc = await player.vc.channel.connect(self_deaf=True)
    player = Player.from_player(player)
    # TODO i hate getting the guild id like this...
    Servers.set_player(player.vc.guild.id, player)

# Moved the logic for skip into here to be used by NowPlayingView and PlayerManagement
async def skip_logic(player: Player, ctx: discord.ApplicationContext):
    """
    Performs all of the complex logic for permitting or denying skips.
    
    Placed here for use in both PlaybackManagement and NowPlayingView
    
    Parameters
    ----------
    player : `Player`
        The player the song belongs to.
    ctx : `discord.ApplicationContext`
        The message ApplicationContext.

    """
    # Get a complex embed for votes
    async def skip_msg(title: str = '', content: str = '', present_tense: bool = True, ephemeral: bool = False) -> None:

        embed = get_embed(ctx, title, content,
                          color=get_random_hex(player.song.id),
                          progress=present_tense)
        embed.set_thumbnail(url=player.song.thumbnail)

        users = ''
        for user in player.song.vote.get():
            users = f'{user.name}, {users}'
        users = users[:-2]
        if present_tense:
            # != 1 because if for whatever reason len(skip_vote) == 0 it will still make sense
            voter_message = f"User{'s who have' if len(player.song.vote) != 1 else ' who has'} voted to skip:"
            song_message = "Song being voted on:"
        else:
            voter_message = f"Vote passed by:"
            song_message = "Song that was voted on:"

        embed.add_field(name="Initiated by:",
                        value=player.song.vote.initiator.mention)
        embed.add_field(name=song_message,
                        value=player.song.title, inline=True)
        embed.add_field(name=voter_message, value=users, inline=False)
        await respond(ctx, embed=embed, ephemeral=ephemeral)

    # If there's not enough people for it to make sense to call a vote in the first place
    # or if this user has authority
    if len(player.vc.channel.members) <= 3 or Pretests.has_song_authority(ctx, player.song):
        player.vc.stop()
        await send(ctx, "Skipped!", ":white_check_mark:")
        return

    votes_required = len(player.vc.channel.members) // 2

    if player.song.vote is None:
        # Create new Vote
        player.song.create_vote(ctx.user)
        await skip_msg("Vote added.", f"{votes_required - len(player.song.vote)}/{votes_required} votes to skip.")
        return

    # If user has already voted to skip
    if ctx.user in player.song.vote.get():
        await skip_msg("You have already voted to skip!", ":octagonal_sign:", ephemeral=True)
        return

    # Add vote
    player.song.vote.add(ctx.user)

    # If vote succeeds
    if len(player.song.vote) >= votes_required:
        await skip_msg("Skip vote succeeded! :tada:", present_tense=False)
        player.song.vote = None
        player.vc.stop()
        return

    await skip_msg("Vote added.", f"{votes_required - len(player.song.vote)}/{votes_required} votes to skip.")


# Makes things more organized by being able to access Utils.Pretests.[name of pretest]
class Pretests:
    """
    A static class containing methods for pre-run state tests.

    ...

    Methods
    -------
    has_discretionary_authority(ctx: `discord.ApplicationContext`):
        Checks if the ctx.user has discretionary authority in the current scenario.
    has_song_authority(ctx: `discord.ApplicationContext`, song: `Song`):
        Checks if the ctx.user has authority over the given song.
    voice_channel(ctx: `discord.ApplicationContext`)
        Checks if all voice channel states are correct.
    player_exists(ctx: `discord.ApplicationContext`):
        Checks if there is a Player registered for the current guild and if voice channel states are correct.
    playing_audio(ctx: `discord.ApplicationContext`)
        Checks if audio is playing in a player for that guild and voice channel states are correct.
    """
    # To be used with control over the Player as a whole
    def has_discretionary_authority(ctx: discord.ApplicationContext) -> bool:
        """
        Checks if the ctx.user has discretionary authority in the current scenario.
        
        Parameters
        ----------
        ctx : `discord.ApplicationContext`
            The ctx to pull ctx.user from.

        Returns
        -------
        `bool`:
            Whether the ctx.user should have discretionary authority.
        """

        if ctx.user.voice and len(ctx.user.voice.channel.members) <= 3:
            return True
        for role in ctx.user.roles:
            if role.name.lower() == 'dj':
                return True
            if role.permissions.manage_channels or role.permissions.administrator:
                return True
        # Force discretionary authority for developers
        if ctx.user.id == 369999044023549962 or ctx.user.id == 311659410109759488:
            return True
        return False

    # To be used for control over a specific song
    def has_song_authority(ctx: discord.ApplicationContext, song: Song) -> bool:
        """
        Checks if the ctx.user has authority over the given song.
        
        Parameters
        ----------
        ctx : `discord.ApplicationContext`
            The ctx to pull ctx.user from.
        song : `Song`
            The song to compare ctx.user to.

        Returns
        -------
        `bool`:
            Whether the ctx.user should have authority over the song.
        """
        if song.requester == ctx.user:
            return True

        return Pretests.has_discretionary_authority(ctx)

    # Checks if voice channel states are right
    async def voice_channel(ctx: discord.ApplicationContext) -> bool:
        """
        Checks if all voice channel states are correct.

        Specifically, this checks if MaBalls is in a voice channel and if the person executing the command is in the same channel.
        
        Parameters
        ----------
        ctx : `discord.ApplicationContext`
            The ctx to check and respond in.

        Returns
        -------
        `True`:
            Will return true in the event that all checks pass.
        `False`:
            Will return false in the event one or more checks fail, this will also use ctx.response to send a response to the message.
        """
        if ctx.guild.voice_client is None:
            await respond(ctx, "MaBalls is not in a voice channel", ephemeral=True)
            return False

        if ctx.user.voice.channel != ctx.guild.voice_client.channel:
            await respond(ctx, "You must be connected to the same voice channel as MaBalls", ephemeral=True)
            return False
        return True

    # Expanded test for if a Player exists
    async def player_exists(ctx: discord.ApplicationContext) -> bool:
        """
        Checks if there is a Player registered for the current guild and if voice channel states are correct.

        Specifically, this checks if voice_channel returns True then checks if the Player exists for that guild.
        
        Parameters
        ----------
        ctx : `discord.ApplicationContext`
            The ctx to check and respond in.

        Returns
        -------
        `True`:
            Will return true in the event that all checks pass.
        `False`:
            Will return false in the event one or more checks fail, this will also use ctx.response to send a response to the message.
        """
        if not await Pretests.voice_channel(ctx):
            return False
        if Servers.get_player(ctx.guild_id) is None:
            await respond(ctx, "This command can only be used while a queue exists", ephemeral=True)
            return False
        return True

    # Expanded test for if audio is currently playing from a Player
    async def playing_audio(ctx: discord.ApplicationContext) -> bool:
        """
        Checks if audio is playing in a player for that guild and voice channel states are correct.

        Specifically, this checks if player_exists and subsequently voice_channel returns True then checks if player.is_playing is True.
        
        Parameters
        ----------
        ctx : `discord.ApplicationContext`
            The ctx to check and respond in.

        Returns
        -------
        `True`:
            Will return true in the event that all checks pass.
        `False`:
            Will return false in the event one or more checks fail, this will also use ctx.response to send a response to the message.
        """
        if not await Pretests.player_exists(ctx):
            return False
        if not Servers.get_player(ctx.guild_id).is_playing():
            await respond(ctx, "This command can only be used while a song is playing.")
            return False
        return True
    
