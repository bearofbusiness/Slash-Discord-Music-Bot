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

Cogs
----
There are cogs available that can be enabled and disabled at will in order to add extensibility to the bot. 
All but `Update` are needed for core functionality.
They can be enabled and disabled via the `.env` with respective keys.

Update
------
The `Update` cog is disabled by default, and when enabled allows a user specified in the `developers` key of the `.env` file to run 
the /update command; which automatically update the bot's libraries to ensure functionality of yt-dlp.
To enable the `Update` cog, change the corresponding value in the `.env` to "true". 
However, this command **only works on linux systems and requires the bot to be 
currently running in a tmux session and a python virtual environment**

Dotenv Configuration
--------------------

Out of the box, the bot will search for a Discord token in the .env named `key`.

### Example key
```dotenv
key="aaaaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.cccccccccccccccccccccccccccccccccccccc"
```
The bot will also search for a list called `developers`, be sure to put your username in that list if you want to have 
full control of the bot. 
### Example developers
```dotenv
developers=111111111111111111,222222222222222222,333333333333333333
```
For a complete example, check the example_env file.
