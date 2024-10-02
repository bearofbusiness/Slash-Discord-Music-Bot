MaBalls
=======
MaBalls is an open-source discord music bot. It is designed to work with YouTube primarily but should work with any non-DRM music.

We used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to parse media and [discord.py](https://github.com/Rapptz/discord.py) to communicate with the discord API.

We host a bot that runs our master branch - its join URL is [here.](https://discord.com/api/oauth2/authorize?client_id=918667870114828288&permissions=3467840&scope=bot)

Installing
----------
**Python 3.10 or higher is required**

Requirements are listed inside the `requirements.txt` file. You must install it using pip on windows or using your package manager on linux. You can also use anaconda for package management.

The main file is `musS_D.py`

The best way to run it is through a console `python3.10 musS_D.py`(set python version as needed)

Dotenv Configuration
--------------------

Out of the box, the bot will search for a discord token in the .env named `key`

### Example .env
```env
key="aaaaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.cccccccccccccccccccccccccccccccccccccc"
```
