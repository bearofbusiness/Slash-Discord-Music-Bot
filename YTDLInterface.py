import asyncio
import yt_dlp
import functools

# Class to make what caused the error more apparent
class YTDLError(Exception):
    pass


class YTDLInterface:

    retrieve_options = {
        'format': 'bestaudio/best',
        'audioformat': 'mp3',
        'yesplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': False,
        'no_warnings': False,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    scrape_options = {
        'format': 'bestaudio/best',
        'audioformat': 'mp3',
        'yesplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': False,
        'no_warnings': False,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'extract_flat':True,
    }

    

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    # Rapidy retrieves shell information surrounding a URL
    @staticmethod
    async def scrape_link(link: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ') -> dict:
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(YTDLInterface.scrape_options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, link, download=False)
            query_result = await loop.run_in_executor(None, partial)
        
        # If yt-dlp threw an error
        if query_result is None:
            raise YTDLError(f'Couldn\'t fetch `{link}`')
        
        return query_result

    # Only called to automatically resolve searches input into scrape_link
    # Pulls information from a yt-dlp accepted URL and returns a Dict containing that information
    @staticmethod
    async def query_link(link: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ') -> dict:
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(YTDLInterface.retrieve_options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, link, download=False)
            query_result = await loop.run_in_executor(None, partial)

        # If yt-dlp threw an error
        if query_result is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(link))

        return query_result


    # Searches for a provided string
    @staticmethod
    async def scrape_search(query: str) -> dict:
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(YTDLInterface.scrape_options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, f'ytsearch5:{query}', download=False)
            query_result = await loop.run_in_executor(None, partial)

        # If yt-dlp threw an error
        if query_result is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(query))

        return query_result

