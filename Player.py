import asyncio
import discord
from Queue import Queue
from YTDLInterface import YTDLInterface


class Player:
    def __init__(self, vc) -> None:
        self.player_event = asyncio.Event()
        self.player_abort = asyncio.Event()
        self.player_skip = asyncio.Event()
        self.player_task = asyncio.create_task(
            self.__player())  # self.player_event

        self.queue = Queue()

        self.song = None  # = self.queue.get(0)#this will error

        self.looping = False
        self.queue_looping = False

        self.vc = vc

    async def __player(self):
        print("Initializing Player.")
        await self.player_event.wait()
        print("Player has been given GO signal")
        # This while will immediately terminate when player_abort is set.
        # If it doesn't abort, swap back to threading.Event instead of asyncio

        # I still haven't properly tested if this abort method works so if it's misbehaving this is first on the chopping block
        while not self.player_abort.is_set():

            # Allows __player to terminate without "aborting"
            while not self.player_skip.is_set():
                
                # Get the top song in queue ready to play
                self.song = self.queue.get(0)
                await self.song.populate()

                # Just to be safe and make sure we don't
                # cut off anything early, do a quick is_playing loop
                while self.vc.is_playing():
                    await asyncio.sleep(1)

                # Begin playing audio into Discord
                await self.song.start()
                self.vc.play(discord.FFmpegPCMAudio(
                    self.song.audio, **YTDLInterface.ffmpeg_options
                ))

                # Sleep player until song ends
                await asyncio.sleep(self.song.duration)


                # If song is looping, continue from top
                if self.looping:
                    continue

                self.queue.remove(0)

                # If we're queue looping, re-add the removed song to top of queue
                if self.queue_looping:
                    self.queue.add(self.song)
                    continue

                # Check if the queue is empty
                if not self.queue.get():
                    # Just to be safe and make sure we don't
                    # cut off anything early, do a quick is_playing loop
                    while self.vc.is_playing():
                        await asyncio.sleep(1)
                    # Abort the player
                    self.player_abort.set()

            self.player_skip.unset()
           

        # Signal to everything else that player has ended
        self.player_abort.set()

    # Start player and return upon it's death
    async def start(self) -> None:
        self.player_event.set()
        await self.player_abort.wait()
        return

    def is_started(self) -> bool:
        return self.player_event.is_set()

    def terminate_player(self) -> None:
        self.player_abort.set()
    
    def skip_player(self) -> None:
        self.player_skip.set()

    def set_loop(self, state: bool) -> None:
        self.looping = state

    def set_queue_loop(self, state: bool) -> None:
        self.queue_looping = state
