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

### Example key
```dotenv
key="aaaaaaaaaaaaaaaaaaaaaaaaaa.bbbbbb.cccccccccccccccccccccccccccccccccccccc"
```
The bot will also search for a list of User IDs called `developers`.  
Users in the `developers` list will always have control of the bot, and (if enabled) **will be able to run /update**
### Example developers
```dotenv
developers=111111111111111111,222222222222222222,333333333333333333
```

Updates
-------

MaBalls requires a constantly up-to-date installation of the downloader, `yt-dlp`  
To help 'automate' these upgrades, [Frostwolf74](https://github.com/Frostwolf74) created an in-place updater that can be triggered from Discord by authorized users.

*Due to security risks and specific dependencies, this functionality is disabled by default* and is limited to users listed in the `developers` key in the `.env`.
### Additional System Dependencies for Updates

For updates to function properly, **Ma must be run in a Linux-based environment** and *within a `.venv`**.  
The following dependencies are required:

- `pip` Python module (within venv)

- `tmux` (system package)

Additionally, **Ma must be launched within a tmux session.** Consider adding a run.sh script for convenience. (feel free to submit a pull request!).

*Note: We are not responsible for any broken systems if you fail to use a `.venv`. It's like using a condom: ignore it at your own risk.*

If you accept the implications, and have the dependencies installed,
### ⚠️Enabling /Update⚠️
Before proceeding, make sure you've read the previous section about dependencies.  
Ignoring them may **break your system**!

To enable the update feature, open `musS_D.py` and uncomment the line `# await self.load_extension("cogs.Update")`, then restart the bot.  
You should see `"Cog Update loaded!"` in the logs.

Ensure your User ID is listed in the `developers` key in the `.env`, and that all dependencies are installed--then you're good to go!
