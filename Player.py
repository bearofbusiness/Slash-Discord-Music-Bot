import asyncio
import discord
import math
import random
import traceback
import time


# Our imports
import Buttons
import Utils
from Queue import Queue
from Song import Song
from YTDLInterface import YTDLInterface
from DB import DB

# Class to make what caused the error more apparent


class VoiceError(Exception):
    """Generic voice error class."""
    pass


class Player:
    """
    A class that handles Song population and playback as well as Queue management for a guild.
    
    If a Player ever has no Song to play it will die, remove itself from the Servers class and disconnect from its vc.

    ...

    Attributes
    ----------
    queue : Queue
        The Queue that the Player is responsible for.
    song : Song | None
        The song that is currently playing, if there is not one this is a NoneType.
        This is slightly innacurate as to when the Player is actually playing audio, is_playing() should be used instead.
    last_np_message: discord.Message | None
        The last automatic now-playing Message the Player has sent.  NoneType if it has not sent one.
    looping : bool
        Whether the Player is looping the currently playing Song.
    queue_looping : bool
        Whether the Player is looping the Queue.
    true_looping : bool
        Whether the Player is shuffling completed Songs back into the Queue.
    vc : discord.VoiceClient
        The VoiceClient this Player is managing.
    send_location : discord.abc.GuildChannel
        The location the bot will send auto Now Playing messages.  Updated every song.

    Methods
    -------
    is_playing():
        Whether the player is playing audio or in-between songs. Pausing the Song does not effect this.
    pause():
        Pauses the player.
    resume():
        Resumes the player
    set_loop(state: bool):
        Sets whether the Player should be looping the Song at song.
    set_true_loop(state: bool):
        Sets whether the Player should be shuffling completed Songs back into the Queue.
    set_queue_loop(state: bool):
        Sets whether the Player should be adding completed Songs to the end of the Queue.
        
    """
    def __init__(self, vc: discord.VoiceClient, song: Song) -> None:
        """
        Creates a Player object.

        Parameters
        ----------
        vc : discord.VoiceClient
            The VoiceClient to bind the Player to
        song : Song
            The Song to initalize the Player with.
        """
        self.player_song_end = asyncio.Event()
        # Immediately set the Event because audio is not currently playing
        self.player_song_end.set()

        self.queue = Queue()
        self.queue.add(song)

        # Shouldn't be set but it fixes a race condition
        #TODO is this still true?
        self.song = song

        self.last_np_message = None

        self.looping = False
        self.queue_looping = False
        self.true_looping = False

        self.vc = vc

        self.send_location = vc.channel if DB.GuildSettings.get(vc.guild.id, setting='np_sent_to_vc') else song.channel

        # Create task to run __player
        self.player_task = asyncio.create_task(
            self.__exception_handler_wrapper(self.__player()))

    # Custom exception handler
    async def __exception_handler_wrapper(self, awaitable) -> any:
        """
        Custom exception handling wrapper to avoid the Player from GBJ-ing itself due to unretrieved Exceptions.

        Parameters
        ----------
        awaitable : any
            The awaitable object to run within the wrapper.

        Return
        ------
        any:
            The result of the awaitable.
        """
        try:
            return await awaitable
        except Exception as e:
            embed = discord.Embed(title="An unrecoverable Exception occurred", description=f"```ansi\n{e}\n```")
            await self.vc.channel.send(embed=embed)
            # Traceback print here so we get the full error without causing an infinite loop of exception raises
            traceback.print_exc()
            await Utils.clean(self)
            

    def __song_complete(self, error=None):
        """
        This method is only used for the after parameter of vc.play(), it needs this specific signature.
        
        Not sure what scenario would cause it to raise a VoiceError but if it does, good luck.
        Other than that this is just to raise the player_song_end flag for __player.
        """
        if error:
            raise VoiceError(str(error))
        self.player_song_end.set()

    async def __player(self) -> None:
        """
        This is where the magic happens.  Contains all of the logic for the playback loop.
        """
        Utils.pront("Player initialized.", "OKGREEN")
        while True:
            # Check if the queue is empty
            if not self.queue.get():
                # Clean up and delete player
                await Utils.clean(self)
                return
            
            # Delete the last now playing if it exists
            if self.last_np_message:
                await self.last_np_message.delete()

            song = self.queue.get(0)

            # If the song has not yet been populated or will expire while playing
            # Pretty sure this will cause worse performance on sources other than youtube because they will try to repopulate every time
            #TODO find a better way for that
            if song.expiry_epoch is not None and song.expiry_epoch - time.time() - song.duration < 30:
                song.expiry_epoch = None

            # Only repopulate YouTube links
            if song.expiry_epoch is None and song.source == "Youtube":
                # Populate the song again to refresh the timer
                try:
                    await song.populate()
                # If anything goes wrong, just skip it. (bad form but I am *not* enumerating every single error that can be raised by yt_dlp here)
                except Exception as e:
                    errored_song = song
                    await errored_song.channel.send(f"Song {errored_song.title} -- {errored_song.uploader} ({errored_song.original_url}) failed to load because of ```ansi\n{e}``` and was skipped.")
                    self.queue.remove(0)
                    continue

                # If even after repopulating, the song was going to pass the expiry time
                if song.expiry_epoch - time.time() - song.duration < 30:
                    await song.channel.send(f"Song {song.title} -- {song.uploader} ({song.original_url}) was unable to load because it would expire before playback completed (too long)")

            del song

            # Set the top song to the playing song
            self.song = self.queue.remove(0)

            # Send the new NP
            embed = Utils.get_now_playing_embed(self)
            self.last_np_message = await self.send_location.send(silent=True, embed=embed, view=Buttons.NowPlayingButtons(self))

            # Clear player_song_end here because this is when we start playing audio again
            self.player_song_end.clear()

            self.song.start()

            # Begin playing audio into Discord
            self.vc.play(discord.FFmpegPCMAudio(
                self.song.audio, **YTDLInterface.ffmpeg_options
            ), after=self.__song_complete)
            # () implicit parenthesis

            # Sleep player until song ends
            await self.player_song_end.wait()

            # If song is looping, re-add song to the top of queue
            if self.looping:
                self.queue.add_at(self.song, 0)        

            # If we're true looping, re-add the song to a random position in queue
            elif self.true_looping:
                if len(self.queue.get()) < 4:
                    self.queue.add(self.song)
                    continue
                queue_length = len(self.queue)
                index = random.randrange(math.ceil(queue_length/4), queue_length)
                self.queue.add_at(self.song, index)

            # If we're queue looping, re-add the removed song to bottom of queue
            elif self.queue_looping:
                self.queue.add(self.song)

            self.song = None

    def is_playing(self) -> bool:
        """
        Whether the player is playing audio or in-between songs. Pausing the Song does not effect this.

        Returns
        -------
        bool:
            True if the Player is playing audio or paused.

            False if the Player is between songs.
        """
        return not self.player_song_end.is_set()

    def pause(self) -> None:
        """
        Pauses the player.
        """
        self.vc.pause()
        self.song.pause()
    
    def resume(self) -> None:
        """
        Resumes the player.
        """
        self.vc.resume()
        self.song.resume()

    def set_loop(self, state: bool) -> None:
        """
        Sets whether the Player should be looping the Song at song.

        Takes priority over true_looping or queue_looping.

        Parameters
        ----------
        state : bool
            Whether the player should be looping or not.
        """
        self.looping = state

    def set_true_loop(self, state: bool) -> None:
        """
        Sets whether the Player should be shuffling completed Songs back into the Queue.

        Takes priority over queue_looping but will be ignored if looping is True.

        Parameters
        ----------
        state : bool
            Whether the player should be true looping or not.
        """
        self.true_looping = state

    def set_queue_loop(self, state: bool) -> None:
        """
        Sets whether the Player should be adding completed Songs to the end of the Queue.

        Will be ignored if true_looping or looping are True.

        Parameters
        ----------
        state : bool
            Whether the player should be queue looping or not.
        """
        self.queue_looping = state
