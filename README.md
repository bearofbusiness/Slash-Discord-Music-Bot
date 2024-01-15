MaBalls
=======
MaBalls is an open-source discord music bot. It is designed to work with YouTube primarily but should work with any non-DRM music.

We used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to parse media and [discord.py](https://github.com/Rapptz/discord.py) to communicate with the discord API.

We host a bot that runs our master branch, its join URL is [here.](https://discord.com/api/oauth2/authorize?client_id=918667870114828288&permissions=3467840&scope=bot)

Installing
----------
**Python 3.10 or higher is required**

Requirements are listed inside the `requirements.txt` file. 

The main file is `musS_D.py`

Dotenv Configuration
--------------------

Out of the box, the bot will search for a discord token in the .env named `key`

### Example .env
```env
key="aaaaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.cccccccccccccccccccccccccccccccccccccc"
```
