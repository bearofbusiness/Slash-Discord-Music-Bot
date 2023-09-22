# Slash-Discord-Music-Bot
MaBalls is an Open-Source discord music bot. It is designed to work with YouTube primarily but should work with any non-DRM music.
---
We used [yt-dlp](https://github.com/yt-dlp/yt-dlp) to parse media and [discord.py](https://github.com/Rapptz/discord.py) to communicate with the discord API.
---
# Setting up the bot
## Step 1
install git and clone the repo or just download the files as a zip. Cloning the repo with git will allow you to get updates easier.
## Step 2
install python if you dont have it you need 3.10 or later (if you want to to use an older version for a reason you will need to modidy the code)
## Step 3
install all the libraries (done in command line using `pip install (name_of_package)`)
- discord.py
- PYNACL
- YT-DLP
- python-dotenv
## Step 4
  create a bot on [discord developer portal](https://discord.com/developers) and copy the token
## Step 5
create a file in the base folder of the bot and call it ".env" copy the bot token in to the file like this `key = "BOT_TOKEN_HERE"`
## Step 6
Run the InitalizeDB.py file. The recomended way to run it is to open a command line and cd to the directory and exicute `python Initalize.py`
## Step 7
Run the musS_D.py file. This file needs to be ran in command line or atleast with a batch or bash script that ends with a pause. This is because it may error and you need to see the error and try to fix it.
