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
XX = '''
#-fnt stands for finished not tested
#-f is just finished
TODO:
    6- fnt alert user when songs were unable to be added inside _playlist()
    5- rearrange functions, their order here decides what order they show up in when people type / in discord
    3- clean up todos in various parts of code
    2- write pydocs
    -make more commands
        1- create add-at(?) (merge with playtop? ask for int instead of bool?)
        1- help #bear //done but needs to be updated
        1- settings #bear
        1- move command #bear 
        1- write pause and play methods in player to consolidate controlls into one place
    -other
        9- add info on permissions to help
        7- fnt DJ role to do most bot functions, users without can still queue songs (! top), join bot to channel, etc.
        5- rename get_embed's content argument to description
        5- right more help including dj role

        


DONE:
    9-f make listener for player.start returning to call clean() // found alternative that probably works better
    9-f fix automatic now_playing messages
    8-f make forceskip admin-only
    8-f make play and playlist only join VC if the provided queries are valid (prevents bot from joining to just do nothing)
    8-f make YTDLInterface.query_link calls cognizant of entries[] and able to handle it's appearance
    8-f likewise, make query_search able to handle a lack of entries[] // Never going to happen; (hopefully) a non issue
    7-fnt create general on_error event method
     - make more commands
        9-f pause #bear //vc.pause() and vc.resume()
        9-f resume #bear
        9-f now #bear
        9-f skip (force skip) #sming
        8-f search #sming
        8-f queue #bear
        8-f remove #bear
        8-f play_top #bear
        7-f remove user's songs from queue
        7-f play_list #sming
        7-f play_list_shuffle #sming
        6-f clear #bear
        5-f shuffle #bear
        4-f loop (queue, song) #bear
        1-f fix queue emojis being backwards
        1-f option to decide if __send_np goes into vc.channel or song.channel #sming
        1-f remove_duplicates #bear (sming finished it)
        1-f remove author's songs from queue when author leaves vc #sming //can't be done until we have settings

     - Be able to play music from youtube
        - play music
        - stop music
    (kind but found a better way)- get downloading to work
     - Be able to join vc and play sound
        - join vc
        - leave vc
        - play sound
    - other
        9-f footer that states the progress of the song #bear
        8-f author doesn't need to vote to skip#sming
        8-f fix auto now playing messages not deleting //found why, it's because the player.wait_until_termination() returns instantly once we tell the player to close
        8-f auto-leave VC if bot is alone #sming
        7-f only generate a player when audio is playing, remove the player_event, force initialization with a Song or Queue
        6-f Implement discord.Button with queue
        5-f access currently playing song via player.song rather than player.queue.top() (maybe remove current song from queue while we're at it?)
        4-f remove unneeded async defs
        3-f make it multi server #bear

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
        self.synced=False

    async def on_ready(self):
        #Checking if database exists

        Utils.pront("trying to create database")
        import InitializeDB
        del InitializeDB
        
        #fixing column values
        Utils.pront("Fixing column values if needed")
        DB.fix_column_values()

        #adding existing servers to database
        Utils.pront("Adding servers to database if any are missing")
        DB.initalize_servers_in_DB(bot.guilds)

        #adding cogs
        await bot.load_extension("cogs.GuildManagement")
        await bot.load_extension("cogs.QueueManagement")
        await bot.load_extension("cogs.PlaybackManagement")
        await bot.load_extension("cogs.PlayerManagement")
        Utils.pront("Cogs loaded!")

        #syncing tree
        Utils.pront("Syncing tree")
        if not self.synced:
            await bot.tree.sync()  # please dont remove just in case i need to sync
        Utils.pront("Tree synced!")

        #setting status
        Utils.pront("Setting bot status")
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"you in {len(bot.guilds):,} Servers."))
        
        Utils.pront("Bot is ready", lvl="OKGREEN")

# Global Variables
bot = Bot()

## EVENT LISTENERS ##

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
    # If we don't care that a voice state was updated
    # because we're not connected to that server anyways >:(
    if member.guild.voice_client is None:
        return
    
    # If it's the bot
    if member == bot.user:
        # If we've been forcibly removed from a VC
        # (this leaves a hanging voice_client)
        if after.channel == None and member.guild.voice_client is not None:
            player = Servers.get_player(member.guild.id)
            # No player? No problem.
            if player is None:
                return
            # If there is one, properly close it up
            else:
                await Utils.clean(player)
                return

    # If the user was in the same VC as the bot and disconnected
    if before.channel == member.guild.voice_client.channel and after.channel != before.channel:
        # If the bot is now alone
        if len(before.channel.members) == 1:
            player = Servers.get_player(member.guild.id)
            if player is None:
                member.guild.voice_client.disconnect()
            else:
                await Utils.clean(player)
        
        # If the bot should purge their queued songs
        if DB.GuildSettings.get(member.guild.id, 'remove_orphaned_songs'):
            player = Servers.get_player(member.guild.id)
            # If there isn't a player, abort
            if player is None:
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
                embed.set_footer(icon_url=player.song.thumbnail,
                    text=f'{"🔂 " if player.looping else ""}{"🔁 " if player.queue_looping else ""}{"♾ " if player.true_looping else ""}\n{Utils.get_progress_bar(player.song)}')
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

# Custom error handler
async def on_tree_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):

    # If a yt_dlp DownloadError was raised
    if isinstance(error.original, yt_dlp.utils.DownloadError):
        await interaction.followup.send(embed=Utils.get_embed(interaction, "An error occurred while trying to parse the link.",
                                                              content=f'```ansi\n{error.original.exc_info[1]}```'))
        # Return here because we don't want to print an obvious error like this.
        return

    # Fallback default error
    await interaction.followup.send(embed=Utils.get_embed(interaction, title="MaBalls ran into Ma issue.", content=f'```ansi\n{error}```', progress=False))
    # Allows entire error to be printed without raising an exception
    # (would create an infinite loop as it would be caught by this function)
    traceback.print_exc()
bot.tree.on_error = on_tree_error



bot.run(key)
