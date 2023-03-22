from discord import Member
from Vote import Vote
from YTDLInterface import YTDLInterface
import time


class Song:
    def __init__(self, interaction, link):
        self.link = link
        self.requester = interaction.user
        self.channel = interaction.channel
        self.vote = None

        # All of these will be populated when the populate() method is called
        self.title = None
        self.uploader = None
        self.audio = None
        self.id = None
        self.thumbnail = None
        self.duration = None
        self.original_url = None

        # Delta time handling variables
        self.start_time = 0
        self.pause_start = 0
        self.pause_time = 0

    # Populate all None fields
    # @classmethod
    async def populate(self) -> None:
        data = await YTDLInterface.query_link(self.link)
        self.title = data.get('title')
        self.uploader = data.get('channel')
        self.audio = data.get('url')
        self.id = data.get('id')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.original_url = data.get('webpage_url')

    def create_vote(self, member: Member) -> None:
        self.vote = Vote()

    @staticmethod
    def parse_duration(duration: int) -> str:
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days} days')
        if hours > 0:
            duration.append(f'{hours} hours')
        if minutes > 0:
            duration.append(f'{minutes} minutes')
        if seconds > 0:
            duration.append(f'{seconds} seconds')

        return ', '.join(duration)

    @staticmethod
    def parse_duration_short_hand(duration: int) -> str:
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days:02d}')
        if hours > 0:
            duration.append(f'{hours:02d}')
        duration.append(f'{minutes:02d}')
        duration.append(f'{seconds:02d}')

        return ':'.join(duration)

    async def start(self) -> None:
        self.start_time = time.time()
        self.pause_time = 0

    async def pause(self) -> None:
        self.pause_start = time.time()

    async def resume(self) -> None:
        self.pause_time += time.time() - self.pause_start
        self.pause_start = None

    async def get_elapsed_time(self) -> int:
        return (time.time() + self.pause_time) - self.start_time

    def __str__(self) -> str:
        return f'{self.title} by {self.uploader}'
