from __future__ import annotations
import asyncio
import discord
import math
import random
import traceback
import time


# Our imports
import Buttons
import Utils
from Servers import Servers
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
    queue : `Queue`
        The Queue that the Player is responsible for.
    song : `Song`
        The song that is playing, or about to play.
        To know when the Player is actually playing audio, is_playing() should be used.
    last_np_message: `discord.Message` | `None`
        The last automatic now-playing Message the Player has sent.  NoneType if it has not sent one.
    looping : `bool`
        Whether the Player is looping the currently playing Song.
    queue_looping : `bool`
        Whether the Player is looping the Queue.
    true_looping : `bool`
        Whether the Player is shuffling completed Songs back into the Queue.
    vc : `discord.VoiceClient`
        The VoiceClient this Player is managing.
    send_location : `discord.abc.GuildChannel`
        The location the bot will send auto Now Playing messages.  Updated every song.

    Methods
    -------
    async clean():
        Cleans up and closes the player.
    is_dead():
        Whether the Player is being cleaned and should not be used.
    is_playing():
        Whether the player is playing audio or in-between songs. Pausing the Song does not effect this.
    pause():
        Pauses the player.
    resume():
        Resumes the player
    set_loop(state: `bool`):
        Sets whether the Player should be looping the Song at song.
    set_true_loop(state: `bool`):
        Sets whether the Player should be shuffling completed Songs back into the Queue.
    set_queue_loop(state: `bool`):
        Sets whether the Player should be adding completed Songs to the end of the Queue.
        
    """
    def __init__(self, vc: discord.VoiceClient, song: Song) -> None:
        """
        Creates a Player object.

        Parameters
        ----------
        vc : `discord.VoiceClient`
            The VoiceClient to bind the Player to.
        song : `Song`
            The Song to initalize the Player with.
        """
        self.player_kill = asyncio.Event()
        self.player_song_end = asyncio.Event()
        # Immediately set the Event because audio is not currently playing
        self.player_song_end.set()

        self.queue = Queue()
        self.queue.add(song)

        self.song = song

        self.last_np_message = None

        self.looping = False
        self.queue_looping = False
        self.true_looping = False

        self.vc = vc

        try:
            self.send_location = vc.channel if DB.GuildSettings.get(vc.guild.id, setting='np_sent_to_vc') else song.channel
        except AttributeError:
            self.send_location = song.channel


        # Create task to run __player
        self.player_task = asyncio.create_task(
            self.__exception_handler_wrapper(self.__player()))

    @classmethod
    def from_player(cls, player: Player) -> Player:
        """Creates a Player out of an existing Player.
        
        Parameters
        ----------
        player : `Player`
            The Player to copy fields from.
            
        Returns
        -------
        Player
            The new Player.
        """
        # Force creation of an empty Player
        self = cls.__new__(cls)
        self.player_kill = asyncio.Event()
        self.player_song_end = asyncio.Event()
        self.player_song_end.set()

        self.queue = player.queue
        self.queue.add_at(player.song, 0)

        self.song = player.song

        self.last_np_message = player.last_np_message

        self.looping = player.looping
        self.queue_looping = player.queue_looping
        self.true_looping = player.true_looping

        self.vc = player.vc

        self.send_location = player.send_location

        # Create task to run __player
        self.player_task = asyncio.create_task(
            self.__exception_handler_wrapper(self.__player()))
        
        return self

    
    # Custom exception handler
    async def __exception_handler_wrapper(self, awaitable) -> any:
        """
        Custom exception handling wrapper to avoid the Player from GBJ-ing itself due to unretrieved Exceptions.

        Parameters
        ----------
        awaitable : `any`
            The awaitable object to run within the wrapper.

        Returns
        -------
        any
            The result of the awaitable.
        """
        try:
            return await awaitable
        # catch any error because we're just printing it here and aborting
        except Exception as e:
            embed = discord.Embed(title="An unrecoverable Exception occurred", description=f"```ansi\n{e}\n```")
            await self.vc.channel.send(embed=embed)
            # Traceback print here so we get the full error without causing an infinite loop of exception raises
            traceback.print_exc()
            await self.clean()
            

    def __song_complete(self, error=None):
        """
        This method is only used for the after parameter of vc.play(), it needs this specific signature.
        
        Not sure what scenario would cause it to raise a VoiceError but if it does, good luck.
        Other than that this is just to raise the player_song_end flag for __player.
        """
        if error:
            raise VoiceError(error)
        self.player_song_end.set()

    
    async def __last_np_message_handler(self):
        """
        Runs logic for the last_np_message variable, deciding whether to delete it, to change it to a breadcrumb, or to do nothing.
        """
        if not self.last_np_message:
            return
        if DB.GuildSettings.get(self.vc.guild.id, setting='song_breadcrumbs'):
            embed = self.last_np_message.embeds[0]
            embed.title = "Song Breadcrumb:"
            embed.set_thumbnail(url=embed.image.url if embed.image else None)
            embed.set_image(url=None)
            embed.set_footer(text="This song has finished playing.  This breadcrumb has been left because of this server's settings.")
            try:
                self.last_np_message = await self.last_np_message.edit(embed=embed, view=None)
            except discord.NotFound:
                Utils.pront("Player's last_np_message was not NoneType but discord returned 404", "ERROR")
            return
        
        try:
            await self.last_np_message.delete()
        except discord.NotFound:
            Utils.pront("Player's last_np_message was not NoneType but discord returned 404", "ERROR")
        finally:
            self.last_np_message = None


    async def __player(self) -> None:
        """
        This is where the magic happens.  Contains all of the logic for the playback loop.
        """
        try:
            Utils.pront("Player initialized.", "OKGREEN")
            while not self.player_kill.is_set():
                # Check if the queue is empty
                if not self.queue.get():
                    # Clean up and delete player
                    Utils.pront('queue empty, killing player')
                    await self.clean()
                    return
                
                # Get the next song in queue
                self.song = self.queue.remove(0)

                # Run logic for the previous np (if it exists)
                await self.__last_np_message_handler()

                # Update send location preference
                try:
                    self.send_location = self.vc.channel if DB.GuildSettings.get(self.vc.guild.id, setting='np_sent_to_vc') else self.song.channel
                except AttributeError:
                    self.send_location = self.song.channel

                # If the song will expire while playing
                if self.song.expiry_epoch is not None and self.song.expiry_epoch - time.time() - self.song.duration < 30:
                    self.song.expiry_epoch = None

                # Only repopulate YouTube links
                if self.song.expiry_epoch is None and self.song.source in ('Youtube', 'Soundcloud'):
                    Utils.pront(f"populating {self.song.title} within player")
                    # Populate the song again to refresh the timer
                    try:
                        await self.song.populate()
                    # If anything goes wrong, just skip it. (bad form but I am *not* enumerating every single error that can be raised by yt_dlp here)
                    except Exception as e:
                        errored_song = self.song
                        await errored_song.channel.send(f"Song {errored_song.title} -- {errored_song.uploader} ({errored_song.original_url}) failed to load because of ```ansi\n{e}``` and was skipped.")
                        continue
                    
                    # If the song gained an expiry epoch (will not happen for soundcloud)
                    if self.song.expiry_epoch:
                        # If even after repopulating, the song was going to pass the expiry time
                        if self.song.expiry_epoch - time.time() - self.song.duration < 30:
                            await self.song.channel.send(f"Song {self.song.title} -- {self.song.uploader} ({self.song.original_url}) was unable to load because it would expire before playback completed (too long)")
                            continue
                

                # Clear player_song_end here because this is when we start playing audio again
                self.player_song_end.clear()

                self.song.start()

                # Begin playing audio into Discord
                self.vc.play(discord.FFmpegPCMAudio(self.song.audio, **YTDLInterface.ffmpeg_options), after=self.__song_complete)
                # () implicit parenthesis

                # Send the new NP
                self.last_np_message = await self.send_location.send(silent=True, embed=Utils.get_now_playing_embed(self), view=Buttons.NowPlayingView(self))

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
        except Exception as e:
            Utils.pront(f'Caught exception {e} in __player method', 'ERROR')
            raise e

    # Cleans up and closes a player
    async def clean(self) -> None:
        """
        Cleans up and closes a player.
        """
        Utils.pront('cleaning')
        if self.player_kill.is_set():
            Utils.pront('Player has already been killed, not cleaning', 'WARNING')
        self.player_kill.set()
        # End await in Player loop so the while completes
        self.player_song_end.set()
        # Immediately remove the Player from Servers to avoid a race condition
        # which leads to the defunct player being re-used
        Servers.remove(self)
        if self.vc.is_connected():
            await self.vc.disconnect()
        # Run logic on the to-be defunct np
        await self.__last_np_message_handler()
        # Needs to be after all awaited logic or the task closing will stop cleaning
        # (if it was initiated by the Player)
        self.player_task.cancel()
        #TODO try putting del self here

    def is_playing(self) -> bool:
        """
        Whether the player is playing audio or in-between songs. Pausing the Song does not effect this.

        Returns
        -------
        bool
            True if the Player is playing audio or paused. False if the Player is between songs.
        """
        return not self.player_song_end.is_set()
    
    def is_dead(self) -> bool:
        return self.player_kill.is_set()

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
        state : `bool`
            Whether the player should be looping or not.
        """
        self.looping = state

    def set_true_loop(self, state: bool) -> None:
        """
        Sets whether the Player should be shuffling completed Songs back into the Queue.

        Takes priority over queue_looping but will be ignored if looping is True.

        Parameters
        ----------
        state : `bool`
            Whether the player should be true looping or not.
        """
        self.true_looping = state

    def set_queue_loop(self, state: bool) -> None:
        """
        Sets whether the Player should be adding completed Songs to the end of the Queue.

        Will be ignored if true_looping or looping are True.

        Parameters
        ----------
        state : `bool`
            Whether the player should be queue looping or not.
        """
        self.queue_looping = state
