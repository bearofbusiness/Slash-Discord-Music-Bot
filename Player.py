import asyncio
import discord

# Our imports
import Utils
from Queue import Queue
from Song import Song
from YTDLInterface import YTDLInterface

# Class to make what caused the error more apparent


class VoiceError(Exception):
    pass


class Player:
    def __init__(self, vc: discord.VoiceClient, song: Song) -> None:
        self.player_event = asyncio.Event()
        self.player_abort = asyncio.Event()
        self.player_song_end = asyncio.Event()
        # Immediately set the Event because audio is not currently playing
        self.player_song_end.set()

        self.queue = Queue()
        self.queue.add(song)

        # Shouldn't be set but it fixes a race condition
        self.song = song

        self.last_np_message = None

        self.looping = False
        self.queue_looping = False

        self.vc = vc

        # Create task to run __player
        self.player_task = asyncio.create_task(
            self.__player())  # self.player_event

    # Used only for the after flag of vc.play(), needs this specific signature
    def song_complete(self, error=None):
        if error:
            raise VoiceError(str(error))
        self.player_song_end.set()

    async def __player(self) -> None:
        Utils.pront("Player initialized.", "OKGREEN")
        while not self.player_abort.is_set():
            # Check if the queue is empty
            if not self.queue.get():
                # Clean up and delete player
                await Utils.clean(self)

            # BE CAREFUL, this song is not self.song!!!
            song = self.queue.get(0)
            embed = discord.Embed(
                title="Preparing next song...",
                description=f"{song.title} -- {song.uploader} is up next.",
                url=song.original_url,
                color=Utils.get_random_hex(song.id)
            )

            embed.set_thumbnail(url=song.thumbnail)
            # If the np message exists, edit it
            if self.last_np_message is not None:
                try:
                    self.last_np_message = await self.last_np_message.edit(embed=embed)
                # If something happened to the now-playing message just send it again
                except discord.errors.NotFound:
                    self.last_np_message = await self.vc.channel.send(embed=embed)
            # Otherwise, create it
            else:
                self.last_np_message = await self.vc.channel.send(embed=embed)
            #del song(?)

            # Get the top song in queue ready to play
            try:
                await self.queue.get(0).populate()
            # If anything goes wrong, just skip it. (bad form but I am *not* enumerating every single error that can be raised by yt_dlp here)
            except Exception as e:
                errored_song = self.queue.get(0)
                await errored_song.channel.send(f"Song {errored_song.title} -- {errored_song.uploader} ({errored_song.original_url}) failed to load because of `{e}` and was skipped.")
                self.queue.remove(0)
                continue

            # Set the now-populated top song to the playing song
            self.song = self.queue.remove(0)

            # Send the new NP
            embed = Utils.get_now_playing_embed(self)
            try:
                self.last_np_message = await self.last_np_message.edit(embed=embed, view=Utils.NowPlayingButtons(self))
            except discord.errors.NotFound:
                self.last_np_message = await self.vc.channel.send(embed=embed)

            # Clear player_song_end here because this is when we start playing audio again
            self.player_song_end.clear()

            self.song.start()

            # Begin playing audio into Discord
            self.vc.play(discord.FFmpegPCMAudio(
                self.song.audio, **YTDLInterface.ffmpeg_options
            ), after=self.song_complete)
            # () implicit parenthesis

            # Sleep player until song ends
            await self.player_song_end.wait()

            # If song is looping, re-add song to the top of queue
            if self.looping:
                self.queue.add_at(self.song, 0)

            # If we're queue looping, re-add the removed song to bottom of queue
            if self.queue_looping:
                self.queue.add(self.song)
                continue

            self.song = None

    def terminate_player(self) -> None:
        self.player_abort.set()

    def is_playing(self) -> bool:
        return not self.player_song_end.is_set()

    def set_loop(self, state: bool) -> None:
        self.looping = state

    def set_queue_loop(self, state: bool) -> None:
        self.queue_looping = state
