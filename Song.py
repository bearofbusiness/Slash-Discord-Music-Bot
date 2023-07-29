import time

from discord import Member, Interaction
from Vote import Vote
from YTDLInterface import YTDLInterface


class Song:
    """
    A class representing a piece of media

    Attributes
    ----------
    link : str
        The exact link provided when initalizing the Song.
    requester : discord.Member
        The Member who requested the Song to be played.
    channel : discord.abc.GuildChannel
        The channel that the song was requested from.
    vote : Vote | None
        The Vote to skip this song, if there is one.
    title : str | None
        The title of the media, if it is available.
    uploader : str | None
        The uploader of the media, if it is available.
        In the case of YouTube this is the channel that uploaded the video.
    audio : str | None
        The URL to the raw audio of the media, if it is available.
    id : str | None
        The unique identifier of the media, ie: a YouTube video ID or SoundCloud ID
    thumbnail : str | None
        The URL to the highest-resolution thumbnail available.
    duration : int | None
        The duration of the media in seconds, if it is available.
    original_url : str | None
        The upstream URL of the media, if it exists.  This may or may not differ from link.    
    
    Class Methods
    -------------
    from_link(interaction: discord.Interaction, link: str):
        Will attempt to automatically initalize a Song with the provided link.
    
    Methods
    -------
    populate():
        Fills the Song with up-to-date information from original_url.
    create_vote(member: discord.Member)
        Creates a vote to track how many users wish to skip the Song.
    start():
        Starts the Song's internal timer for it's elapsed time.
    pause():
        Alerts the Song that it has been paused to keep it's elapsed time accurate.
    resume():
        Alerts the Song that it has been resumed to keep it's elapsed time accurate.
    get_elapsed_time():
        Gets the Song's elapsed time in seconds.

    Static Methods
    --------------
    parse_duration(duration : int | None):
        Parses a duration in seconds into a longer, human readable format.
    parse_duration_short_hand(duration : int | None):
        Parses a duration in seconds into a shorter human readable xx:xx:xx:xx format.
    """
    def __init__(self, interaction: Interaction, link: str, dict: dict):
        """
        Creates a Song from a dictionary containing specific key:value pairs that match the output of yt-dlp.

        Parameters
        ----------
        interaction : discord.Interaction
            The Interaction that created the Song.
        link : str
            The raw URL or query that created the Song.
        dict : dict
            The dict containing yt-dlp's output.
        """
        self.link = link
        self.requester = interaction.user
        self.channel = interaction.channel
        self.vote = None

        # If there's an unexpected list of entries
        if dict.get('entries') is not None and len(dict.get('entries')) > 0:
            # Get the first result and continue as normal
            dict = dict.get('entries')[0]

        # Try to get a thumbnail
        if dict.get('thumbnails'):
            self.thumbnail = dict.get('thumbnails')[-1].get('url')
        else:
            self.thumbnail = None

        # Try different method to get URL
        if dict.get('webpage_url'):
            self.original_url = dict.get('webpage_url')
        else:
            self.original_url = dict.get('url')

        self.title = dict.get('title')
        self.uploader = dict.get('channel')
        self.audio = dict.get('url')
        self.id = dict.get('id')
        self.duration = dict.get('duration')

        # Delta time handling variables
        self.start_time = 0
        self.pause_start = 0
        self.pause_time = 0

    @classmethod
    async def from_link(cls, interaction: Interaction, link: str):
        """
        Creates a Song from the provided link.

        Parameters
        ----------
        interaction : discord.Interaction
            The Interaction that created the Song.
        link : str
            The URL the method should try to pull information from.
        """
        song = cls(interaction, link, {'webpage_url': link})
        await song.populate()
        return song

    # Populate all None fields
    async def populate(self) -> None:
        """
        Fills the Song with up-to-date information from original_url.
        Necessary with YouTube media after a certain amount of time, as the audio URL from yt-dlp expires.
        """
        data = await YTDLInterface.scrape_link(self.original_url)
        # If there's an unexpected list of entries
        if data.get('entries') is not None and len(data.get('entries')) > 0:
            # Get the first result and continue as normal
            data = data.get('entries')[0]
        self.title = data.get('title')
        self.uploader = data.get('channel')
        self.audio = data.get('url')
        self.id = data.get('id')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.original_url = data.get('webpage_url')

    def create_vote(self, member: Member) -> None:
        """
        Creates a vote to track how many users wish to skip the Song.

        Parameters
        ----------
        member : discord.Member
            The Member who is initiating the Vote.
        """
        self.vote = Vote(member)

    def start(self) -> None:
        """
        Starts the Song's internal timer for it's elapsed time.
        """
        print('Starting song timer')
        self.start_time = time.time()
        self.pause_time = 0

    def pause(self) -> None:
        """
        Alerts the Song that it has been paused to keep it's elapsed time accurate.
        """
        self.pause_start = time.time()

    def resume(self) -> None:
        """
        Alerts the Song that it has been resumed to keep it's elapsed time accurate.
        """
        self.pause_time += time.time() - self.pause_start
        self.pause_start = 0

    def get_elapsed_time(self) -> int:
        """
        Gets the Song's elapsed time in seconds.

        Returns
        -------
        int:
            The number of seconds that the song has played for.
        """
        return time.time() - (self.start_time + self.pause_time + ((time.time() - self.pause_start)if self.pause_start else 0))

    @staticmethod
    def parse_duration(duration: int | None) -> str:
        """
        Parses a duration in seconds into a longer, human readable format.

        Parameters
        ----------
        duration : int | None
            The duration in seconds.
            Accepts a NoneType for redundancy.

        Returns
        -------
        str:
            Human readable x days x hours x minutes x seconds format of the duration.
        """
        if duration is None:
            return 'Unknown'
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
    def parse_duration_short_hand(duration: int | None) -> str:
        """
        Parses a duration in seconds into a shorter, human readable format.

        Parameters
        ----------
        duration : int | None
            The duration in seconds.
            Accepts a NoneType for redundancy.

        Returns
        -------
        str:
            Human readable xx:xx:xx:xx format of the duration.
        """
        if duration is None:
            return '0'
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

    def __str__(self) -> str:
        return f'{self.title} by {self.uploader}'
