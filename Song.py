from YTDLInterface import YTDLInterface


class Song:
    def __init__(self, interaction, link):
        self.link = link
        self.requester = interaction.user
        self.channel = interaction.channel

        # All of these will be populated when the populate() method is called
        self.title = None
        self.channel = None
        self.audio = None
        self.id = None
        self.thumbnail = None
        self.duration = None
        self.original_url = None

    # Populate all None fields
    # @classmethod
    async def populate(self) -> None:
        data = await YTDLInterface.query_link(self.link)
        self.title = data.get('title')
        self.channel = data.get('channel')
        self.audio = data.get('url')
        self.id = data.get('id')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.original_url = data.get('webpage_url')

    @staticmethod
    def parse_duration(duration: int) -> str:
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)