import asyncio
import yt_dlp
import functools

# Generic post-process error class
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
        return await YTDLInterface.__call_dlp(YTDLInterface.scrape_options, link)

    # Only called to automatically resolve searches input into scrape_link
    # Pulls information from a yt-dlp accepted URL and returns a Dict containing that information
    @staticmethod
    async def query_link(link: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ') -> dict:
        return await YTDLInterface.__call_dlp(YTDLInterface.retrieve_options, link)


    # Searches for a provided string
    @staticmethod
    async def scrape_search(query: str) -> dict:
        return await YTDLInterface.__call_dlp(YTDLInterface.scrape_options, f'ytsearch5:{query}')

    # Private method to condense all the others
    @staticmethod
    async def __call_dlp(options: dict, link: str):
        # Define asyncio loop
        loop = asyncio.get_event_loop()

        with yt_dlp.YoutubeDL(options) as ytdlp:
            # Define ytdlp command within a partial to be able to run it within run_in_executor
            partial = functools.partial(
                ytdlp.extract_info, link, download=False)
            query_result = await loop.run_in_executor(None, partial)


        # Might work, might break links
        if query_result.get('entries') is not None:
            if len(query_result.get('entries')) == 0:
                raise YTDLError(f'Couldn\'t fetch `{link}`')

        return query_result