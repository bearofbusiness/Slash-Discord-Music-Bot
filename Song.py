import time

from discord import Member
from Vote import Vote
from YTDLInterface import YTDLInterface


class Song:
    def __init__(self, interaction, link, dict):
        self.link = link
        self.requester = interaction.user
        self.channel = interaction.channel
        self.vote = None

        self.title = dict.get('title')
        self.uploader = dict.get('uploader')
        self.audio = dict.get('audio')
        self.id = dict.get('id')
        self.thumbnail = dict.get('thumbnail')
        self.duration = dict.get('duration')
        self.original_url = dict.get('original_url')

        # Delta time handling variables
        self.start_time = 0
        self.pause_start = 0
        self.pause_time = 0

    @classmethod
    def from_link(cls, interaction, link):
        return cls(interaction, link, Song.get_empty_song_dict())

    # Populate all None fields
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
        self.vote = Vote(member)

    @staticmethod
    def get_empty_song_dict():
        return {
            'title': None,
            'uploader': None,
            'audio': None,
            'id': None,
            'thumbnail': None,
            'duration': None,
            'original_url': None

        }

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

    def start(self) -> None:
        print('Starting song timer')
        self.start_time = time.time()
        self.pause_time = 0

    def pause(self) -> None:
        self.pause_start = time.time()

    def resume(self) -> None:
        self.pause_time += time.time() - self.pause_start
        self.pause_start = 0

    def get_elapsed_time(self) -> int:
        return (time.time()) - (self.start_time + self.pause_time + ((time.time() - self.pause_start)if self.pause_start else 0))

    def __str__(self) -> str:
        return f'{self.title} by {self.uploader}'
