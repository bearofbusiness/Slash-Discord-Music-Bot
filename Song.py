from YTDLInterface import YTDLInterface


class Song:
    def __init__(self, interaction, link):
        self.link = link
        self.requester = interaction.user
        self.channel = interaction.channel

        # All of these will be populated when the populate() method is called
        self.title = None
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


if __name__ == "__main__":  # for debuging
    import asyncio

    class fake_interaction:
        def __init__(self):
            self.user = "fake_user"
            self.channel = "fake_channel"

    async def main():
        song = Song(fake_interaction(),
                    'https://youtu.be/HNn1N6-2euk')
        await song.populate()
        print(song.title)
        print(song.audio)
        print(song.id)
        print(song.thumbnail)
        print(song.duration)
        print(song.original_url)
        print(song.parse_duration(song.duration))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
