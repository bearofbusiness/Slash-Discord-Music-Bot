import asyncio
import logging
import subprocess
import sys

import discord
import os
import traceback
from discord.ext import commands
from dotenv import load_dotenv


# importing other classes from other files
import Utils
import Buttons
from Pages import Pages
from Servers import Servers
from DB import DB

# imports for error type checking
import yt_dlp
# needed to add it to a var bc of pylint on my laptop but i delete it right after

handler = logging.FileHandler(filename='recent.log', encoding='utf-8', mode='w')

XX = '''
#-fnt stands for finished not tested
TODO:
    6- make a new way to limit mixes to 50 songs
    5-f make sure all pydocs are tabbed properly (parameters are tabbed in, same with returns)
    3- clean up todos in various parts of code
    2- write more pydocs
    -make more commands
        1- create add-at(?) (merge with playtop? ask for int instead of bool?)#no make it a different thing
        1- playnow puts the current song at top of queue and plays the this song
        1- help #bear //done but needs to be updated
        1-fnt<kinda> move command #bear 
        1- write pause and play methods in player to consolidate controlls into one place
        1- implement a suggestions command that goes to a google forms or something.
    -other
        9- add info on permissions to help
        5- rename get_embed's content argument to description
        5- right more help including dj role

        
'''
del XX

load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')


class Bot(commands.Bot):  # initiates the bots intents and on_ready event
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix="​", intents=intents)

    async def setup_hook(self):
        #adding cogs
        await self.load_extension("cogs.GuildManagement")
        await self.load_extension("cogs.QueueManagement")
        await self.load_extension("cogs.PlaybackManagement")
        await self.load_extension("cogs.PlayerManagement")
        #await self.load_extension("cogs.DebugCog")
        Utils.pront("Cogs loaded!")

        # Database loading
        Utils.pront("Attempting to locate or create database")
        DB.create_tables()
        

    async def on_ready(self):

        # Command syncing
        Utils.pront("Syncing tree")
        await self.tree.sync()
        Utils.pront("Tree synced!")

        # Fixing column values
        Utils.pront("Fixing column values if needed")
        DB.fix_column_values()
        
        # Adding existing servers to database
        Utils.pront("Adding servers to database if any are missing")
        DB.initalize_servers_in_DB(bot.guilds)

        # Setting status
        Utils.pront("Setting bot status")
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"you in {len(bot.guilds):,} servers."))
        
        Utils.pront("Bot is ready", lvl="OKGREEN")
        stringBuilder = ""
        for i in self.guilds:
            stringBuilder += str(i.name) + "\n"
        print(stringBuilder)

    async def on_resumed(self):
        Utils.pront("Updating bot status")
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"you in {len(bot.guilds):,} servers."))

# Initialize bot object
bot = Bot()

# Custom error handler
@bot.tree.error
async def on_tree_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):

    # If a yt_dlp DownloadError was raised
    if isinstance(error.original, yt_dlp.utils.DownloadError):
        await interaction.followup.send(embed=Utils.get_embed(interaction, "An error occurred while trying to parse the link.",
                                                              content=f'```ansi\n{error.original.exc_info[1]}```'))
        # Return here because we don't want to print an obvious error like this.
        return

    # Fallback default error
    await interaction.channel.send(embed=Utils.get_embed(interaction, title="MaBalls ran into Ma issue.", content=f'```ansi\n{error}```', progress=False))
    # Allows entire error to be printed without raising an exception
    # (would create an infinite loop as it would be caught by this function)
    traceback.print_exc()


## EVENT LISTENERS ##
#TODO walk through this logic again
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
    # If we don't care that a voice state was updated
    # because we're not connected to that server anyways >:(
    if member.guild.voice_client is None:
        return
    
    # If it's the bot
    if member == bot.user:
        # if we're disconnecting
        if after.channel == None:
        # If we've been forcibly removed from a VC
        # (this leaves a hanging voice_client)
            if member.guild.voice_client is not None:
                Utils.pront("Bot was disconnected from VC")
                player = Servers.get_player(member.guild.id)
                # Clean up the player if it exists
                if player is not None:
                    await player.clean()
        return

    # If the user was in the same VC as the bot and disconnected
    if before.channel == member.guild.voice_client.channel and after.channel != before.channel:
        # If the bot is now alone
        if len(before.channel.members) == 1:
            player = Servers.get_player(member.guild.id)
            if player is None:
                await member.guild.voice_client.disconnect()
            else:
                await player.clean()
        
        # If the bot should purge duplicate queued songs
        if DB.GuildSettings.get(member.guild.id, 'remove_orphaned_songs'):
            player = Servers.get_player(member.guild.id)

            # If there isn't a player, abort
            if player is None:
                Utils.pront("Attempted to purge queue, missing player", lvl="WARNING")
                return

            # Loop through songs in queue and remove duplicates
            removed = 0
            for i in range(len(player.queue.get()) - 1, 0, -1):
                pass
                if player.queue.get(i).requester == member:
                    player.queue.remove(i)
                    removed += 1

            # If songs were removed, let the users know.
            if removed != 0:
                embed = discord.Embed(
                    title=f'Removed {removed} song{"" if removed == 1 else "s"} queued by user {member.mention}.'
                )
                if player.is_playing():
                    embed.set_footer(icon_url=player.song.thumbnail,
                        text=f'{"🔂 " if player.looping else ""}{"🔁 " if player.queue_looping else ""}{"♾ " if player.true_looping else ""}')
                await player.send_location.send(embed=embed)



@bot.event
async def on_guild_join(guild: discord.Guild)-> None:
    DB.GuildSettings.create_new_guild(guild.id)
    Utils.pront(f"Added {guild.name} to database")

@bot.event
async def on_guild_remove(guild: discord.Guild)-> None:
    DB.GuildSettings.remove_guild(guild.id)
    Utils.pront(f"Removed {guild.name} from database")

@bot.tree.command(name="help", description="Shows the help menu")
async def _help(interaction: discord.Interaction) -> None:
    embed = discord.Embed.from_dict(Pages.get_main_page())
    await interaction.response.send_message(embed=embed, view=Buttons.HelpView(), ephemeral=True)


@bot.tree.command(
    name="update",
    description="Update yt-dlp to nightly",
)
async def update(interaction: discord.Interaction):
    """
        This command REQUIRES python pip and tmux, this command also only works after all required packages have already been installed.
        This simply updates those existing packages and forces yt-dlp to be on the latest nightly branch.
    """

    await interaction.response.defer(thinking=True)
    await interaction.followup.send("Updating yt-dlp and restarting bot", ephemeral=True)

    # Paths and names
    BOT_DIR = os.getcwd()
    VENV_PYTHON = f"{BOT_DIR}/.venv/bin/python"
    YT_DLP_NEW_VERSION = ""

    try:
        # Get current tmux session name for deletion later
        TMUX_OLD = subprocess.run(
            ["tmux", "display-message", "-p", "#S"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Run pip upgrade inside venv for all venv packages and update yt-dlp to nightly
        p1 = subprocess.run([
            "python", "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)

        while p1.returncode is not None:
            if p1.returncode == 0:
                await interaction.channel.send("Finished pip update")
                break

        subprocess.run([
            "touch", f"{BOT_DIR}/packages.txt"
        ], check=True)

        subprocess.run([
            "pip", "freeze", "|", "cut", "-d", "'='", "-f", "1", "|", "sort", "-u", ">", "packages.txt"
        ], check=True)

        p2 = subprocess.run([
            "pip", "install", "--upgrade", "-r", "packages.txt"
        ], check=True)

        while p2.returncode is not None:
            if p2.returncode == 0:
                await interaction.channel.send("Finished venv packages update")
                break

        p3 = subprocess.run([
            f"{VENV_PYTHON}", "-m", "pip", "install", "--upgrade", "--force-reinstall", "git+https://github.com/yt-dlp/yt-dlp.git"
        ], check=True)

        YT_DLP_NEW_VERSION = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        while p3.returncode is not None:
            if p3.returncode == 0:
                await interaction.channel.send("Finished yt-dlp update to " + YT_DLP_NEW_VERSION)
                break

        TMUX_NEW = "frostyslashdiscord-" + YT_DLP_NEW_VERSION

        # Create new tmux session and start the bot in it
        subprocess.run([
            "tmux", "new-session", "-d", "-s", TMUX_NEW,
            f"bash -c 'cd {BOT_DIR} && source .venv/bin/activate && python musS_D.py'"
        ], check=True)

        await interaction.channel.send("Finished installing all packages.\nTerminating old process")

        if TMUX_OLD:
            subprocess.run(["tmux", "kill-session", "-t", TMUX_OLD], check=False)

    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise e
    except Exception as e:
        raise e


bot.run(key, log_handler=handler, log_level=logging.INFO, root_logger=True)