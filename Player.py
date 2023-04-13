import asyncio
import discord

# Our imports
import Utils
from Queue import Queue
from YTDLInterface import YTDLInterface

# Class to make what caused the error more apparent
class VoiceError(Exception):
    pass


class Player:
    def __init__(self, vc: discord.VoiceClient) -> None:
        self.player_event = asyncio.Event()
        self.player_abort = asyncio.Event()
        self.player_song_end = asyncio.Event()
        self.player_task = asyncio.create_task(
            self.__player())  # self.player_event

        self.queue = Queue()

        self.song = None  # = self.queue.get(0)#this will
        # To avoid ^ erroring maybe force Player to be initialized with a Song or Queue?

        self.last_np_message = None

        self.looping = False
        self.queue_looping = False

        self.vc = vc
        
    # Used only for the after flag of vc.play(), needs this specific signature
    def song_complete(self, error=None):
        if error:
            raise VoiceError(str(error))
        self.player_song_end.set()

    async def __player(self) -> None:
        print("Initializing Player.")

        await self.player_event.wait()
        print("Player has been given GO signal")
        # This while will immediately terminate when player_abort is set.

        # I still haven't properly tested if this abort method works so if it's misbehaving this is first on the chopping block
        while not self.player_abort.is_set():
            self.player_song_end.clear()
            # Get the top song in queue ready to play
            await self.queue.top().populate()

            # Set the now-populated top song to the playing song
            self.song = self.queue.top()


            embed = Utils.get_now_playing_embed(self)

            # Delete last now_playing if there is one
            if self.last_np_message is not None:
                await self.last_np_message.delete()
            self.last_np_message = await self.vc.channel.send(embed=embed)


            self.song.start()

            # Begin playing audio into Discord
            self.vc.play(discord.FFmpegPCMAudio(
                self.song.audio, **YTDLInterface.ffmpeg_options
            ), after=self.song_complete)
            # () implicit parenthesis

            # Sleep player until song ends
            await self.player_song_end.wait()
            # If song is looping, continue from top
            if self.looping:
                continue

            self.queue.remove(0)

            # If we're queue looping, re-add the removed song to bottom of queue
            if self.queue_looping:
                self.queue.add(self.song)
                continue

            # Check if the queue is empty
            if not self.queue.get():
                # Wait until it has a song inside it again
                await self.queue.wait_until_has_songs()

    # Raise flag to start the player
    async def start(self) -> None:
        self.player_event.set()
        return

    def is_started(self) -> bool:
        return self.player_event.is_set()

    def terminate_player(self) -> None:
        self.player_abort.set()


    def is_playing(self) -> bool:
        return not self.player_song_end.is_set()

    def set_loop(self, state: bool) -> None:
        self.looping = state

    def set_queue_loop(self, state: bool) -> None:
        self.queue_looping = state
