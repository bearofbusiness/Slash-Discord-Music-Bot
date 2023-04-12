import asyncio
import yt_dlp
import functools

# Class to make what caused the error more apparent
class YTDLError(Exception):
    pass


class YTDLInterface:
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    # Pulls information from a yt-dlp accepted URL and returns a Dict containing that information

    @staticmethod
    async def query_link(link: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ') -> dict:
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(YTDLInterface.options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, link, download=False)
            query_result = await loop.run_in_executor(None, partial)

        # If yt-dlp threw an error
        if not query_result.get('title'):
            raise YTDLError('Couldn\'t fetch `{}`'.format(link))

        return query_result

    # Searches for a provided string
    @staticmethod
    async def query_search(query: str) -> dict:
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(YTDLInterface.options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, f'ytsearch5:{query}', download=False)
            query_result = await loop.run_in_executor(None, partial)

        if not query_result.get('entries'):
            raise YTDLError('No matches found for `{}`'.format(query))

        return query_result
