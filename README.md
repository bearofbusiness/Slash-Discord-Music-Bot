MaBalls
=======
MaBalls is an open-source discord music bot. It is designed to work with YouTube primarily but should work with any non-DRM media.

We used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to parse media and [discord.py](https://github.com/Rapptz/discord.py) to communicate with the discord API.

We host a bot that runs our master branch - its join URL is [here.](https://discord.com/api/oauth2/authorize?client_id=918667870114828288&permissions=3467840&scope=bot)

Installing
----------

**[Python 3.10 or higher is required](https://www.python.org/downloads/)**

Requirements are listed inside the `requirements.txt` file.

The main file is `musS_D.py`

If you're new to this, don't worry! We have* an in-depth install guide [here.](yyyyyyy.info)

*The guide has yet to be written. The link takes you to one of *the* sites on the internet of all time.

Dotenv Configuration
--------------------

Out of the box, the bot will search for a Discord token in the .env named `key`.

### Example .env
```env
key="aaaaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.cccccccccccccccccccccccccccccccccccccc"
```
