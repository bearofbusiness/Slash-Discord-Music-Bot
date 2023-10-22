import discord
import random
from discord.ext import commands
from discord import app_commands

import Buttons
import Utils
from YTDLInterface import YTDLInterface
from Player import Player
from Servers import Servers
from Song import Song
from YTDLInterface import YTDLInterface
from DB import DB

class QueueManagement(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="play", description="Plays a song from youtube(or other sources somtimes) in the voice channel you are in")
    async def play(self, interaction: discord.Interaction, link: str, top: bool = False) -> None:
        # Check if author is in VC
        if interaction.user.voice is None:
            await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
            return

        # Check if author is in the *right* vc if it applies
        if interaction.guild.voice_client is not None and interaction.user.voice.channel != interaction.guild.voice_client.channel:
            await interaction.response.send_message("You must be in the same voice channel in order to use MaBalls", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        # create song
        scrape = await YTDLInterface.scrape_link(link)
        song = Song(interaction, link, scrape)

        # Check if song didn't initialize properly via scrape
        if song.title is None:
            # If it didn't, query the link instead (resolves searches in the link field)
            query = await YTDLInterface.query_link(link)
            song = Song(interaction, query.get('original_url'), query)

        # If not in a VC, join
        if interaction.guild.voice_client is None:
            await interaction.user.voice.channel.connect(self_deaf=True)

        # If player does not exist, create one.
        if Servers.get_player(interaction.guild_id) is None:
            Servers.add(interaction.guild_id, Player(
                interaction.guild.voice_client, song))
            position = 0

        # If it does, add the song to queue
        elif top:
            if not Utils.Pretests.has_discretionary_authority(interaction):
                await interaction.followup.send(embed=Utils.get_embed(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information."))
                return
            Servers.get_player(interaction.guild_id).queue.add_at(song, 0)
            position = 1
        else:
            Servers.get_player(interaction.guild_id).queue.add(song)
            position = len(Servers.get_player(interaction.guild_id).queue.get())
            

        embed = Utils.get_embed(
            interaction,
            title=f'[{position}] Added to Queue:',
            url=song.original_url,
            color=Utils.get_random_hex(song.id)
        )
        embed.add_field(name=song.uploader, value=song.title, inline=False)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.add_field(name='Duration:', value=Song.parse_duration(song.duration))
        embed.set_thumbnail(url=song.thumbnail)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="playlist", description="Adds a playlist to the queue")
    async def playlist(self, interaction: discord.Interaction, link: str, shuffle: bool = False) -> None:
        match DB.GuildSettings.get(interaction.guild_id, 'allow_playlist'):
            # False
            case 0:
                await interaction.response.send_message("Playlists are disabled on this server", ephemeral=True)
                return
            # True
            case 1:
                pass
            # DJ Only
            case 2:
                if not Utils.Pretests.has_discretionary_authority(interaction):
                    await interaction.response.send_message(embed=Utils.get_embed(interaction, title='Insufficient permissions!', 
                            content="Playlists are DJ-only in this server!  Please refer to /help for more information."))
                    return
            case default:
                raise NotImplementedError(f'Invalid value gathered from DB for allow_playlist ({default})')
            
        # Check if author is in VC
        if interaction.user.voice is None:
            await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
            return

        # Check if author is in the *right* vc if it applies
        if interaction.guild.voice_client is not None and interaction.user.voice.channel != interaction.guild.voice_client.channel:
            await interaction.response.send_message("You must be in the same voice channel in order to use MaBalls", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        playlist = await YTDLInterface.skim_playlist(link)

        if playlist.get('_type') != "playlist":
            await interaction.followup.send(embed=Utils.get_embed(interaction, "Not a playlist."), ephemeral=True)
            return

        # Take the extracted webpage url and parse off of that
        playlist = await YTDLInterface.scrape_link(playlist.get('webpage_url'))

        # Might not proc, there for extra protection
        if len(playlist.get("entries")) == 0:
            await interaction.followup.send("Playlist Entries [] empty.")

        # If not in a VC, join
        if interaction.guild.voice_client is None:
            await interaction.user.voice.channel.connect(self_deaf=True)

        # Shuffle the entries[] within playlist before processing them
        if shuffle:
            random.shuffle(playlist.get("entries"))

        entries = playlist.get("entries")

        # If the player doesn't exist, make one
        if Servers.get_player(interaction.guild_id) is None:
            # Get the top song and create a Player from it
            song = Song(interaction, link, entries[0])
            Servers.add(interaction.guild_id, Player(
                    interaction.guild.voice_client, song))
            entries.pop(0)
        
        songs = []

        for entry in entries:
            # Feed the Song the entire entry, saves time by not needing to create and fill a dict
            song = Song(interaction, link, entry)
            songs.append(song)
        
        # Double check that there were other entries to add
        if songs:
            Servers.get_player(interaction.guild_id).queue.add(songs)

        embed = Utils.get_embed(
            interaction,
            title='Added playlist to Queue:',
            url=playlist.get('original_url'),
            color=Utils.get_random_hex(playlist.get('id'))
        )
        embed.add_field(name=playlist.get('uploader'), value=playlist.get('title'))
        embed.add_field(
            name='Length:', value=f'{playlist.get("playlist_count")} songs')
        embed.add_field(name='Requested by:', value=interaction.user.mention)

        # Get the highest resolution thumbnail available
        if playlist.get('thumbnails'):
            thumbnail = playlist.get('thumbnails')[-1].get('url')
        else:
            thumbnail = playlist.get('entries')[0].get('thumbnails')[-1].get('url')
        embed.set_thumbnail(url=thumbnail)

        await interaction.followup.send(embed=embed)

        # Once all is said and done, start the populator thread
        Utils.populate_song_list(songs, interaction.guild_id)

    @app_commands.command(name="search", description="Searches YouTube for a given query")
    async def search(self, interaction: discord.Interaction, query: str) -> None:
        # Check if author is in VC
        if interaction.user.voice is None:
            await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
            return

        # Check if author is in the *right* vc if it applies
        if interaction.guild.voice_client is not None and interaction.user.voice.channel != interaction.guild.voice_client.channel:
            await interaction.response.send_message("You must be in the same voice channel in order to use MaBalls", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        query_result = await YTDLInterface.scrape_search(query)

        embeds = []
        embeds.append(Utils.get_embed(interaction,
                                    title="Search results:",
                                    ))
        for i, entry in enumerate(query_result.get('entries')):
            embed = Utils.get_embed(interaction,
                                    title=f'`[{i+1}]`  {entry.get("title")} -- {entry.get("channel")}',
                                    url=entry.get('url'),
                                    color=Utils.get_random_hex(
                                        entry.get("id"))
                                    )
            embed.add_field(name='Duration:', value=Song.parse_duration(
                entry.get('duration')), inline=True)
            embed.set_thumbnail(url=entry.get('thumbnails')[-1].get('url'))
            embeds.append(embed)

        await interaction.followup.send(embeds=embeds, view=Buttons.SearchSelection(query_result))

    @app_commands.command(name="queue", description="Shows the current queue")
    async def queue(self, interaction: discord.Interaction, page: int = 1) -> None:
        if not await Utils.Pretests.player_exists(interaction):
            return
        # Convert page into non-user friendly (woah scary it starts at 0)(if only we were using lua)
        page -= 1
        player = Servers.get_player(interaction.guild_id)
        if not player.queue.get():
            await Utils.send(interaction, title='Queue is empty!', ephemeral=True)
            return

        qb = Buttons.QueueButtons(page=page)

        await interaction.response.send_message(embed=qb.get_queue_embed(interaction), view=qb)

    @app_commands.command(name="shuffle", description="Shuffles the queue")
    async def shuffle(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.player_exists(interaction):
            return
        player = Servers.get_player(interaction.guild_id)
        # If there's enough people, require authority to shuffle
        if len(player.vc.channel.members) > 4:
            if not Utils.Pretests.has_discretionary_authority(interaction):
                await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
                return
                
        player.queue.shuffle()
        await interaction.response.send_message('🔀 Queue shuffled')

    @app_commands.command(name="remove", description="Removes a song from the queue")
    async def remove(self, interaction: discord.Interaction, number_in_queue: int) -> None:
        if not await Utils.Pretests.player_exists(interaction):
            return
        
        # Convert to non-human-readable only if it's positive
        if number_in_queue > 0:
            # In this scenario 0 or 1 will mean the top song in queue
            number_in_queue -= 1
        song = Servers.get_player(interaction.guild_id).queue.get(number_in_queue)

        if song is None:
            await Utils.send(interaction, "Queue index does not exist.")
            return
        
        if not Utils.Pretests.has_song_authority(interaction, song):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return

        removed_song = Servers.get_player(
            interaction.guild_id).queue.remove(number_in_queue)
        embed = discord.Embed(
            title='Removed from Queue:',
            url=removed_song.original_url,
            color=Utils.get_random_hex(removed_song.id)
        )
        embed.add_field(name=removed_song.uploader,
                        value=removed_song.title, inline=False)
        embed.add_field(name='Requested by:',
                        value=removed_song.requester.mention)
        embed.add_field(name='Duration:',
                        value=Song.parse_duration(removed_song.duration))
        embed.set_thumbnail(url=removed_song.thumbnail)
        embed.set_author(name=removed_song.requester.display_name,
                        icon_url=removed_song.requester.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="removeuser", description="Removes all of the songs added by a specific user")
    async def remove_user(self, interaction: discord.Interaction, member: discord.Member):
        if not await Utils.Pretests.player_exists(interaction):
            return
        
        if not Utils.Pretests.has_discretionary_authority(interaction):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        
        queue = Servers.get_player(interaction.guild.id).queue

        removed = []
        for i in range(len(queue.get()) - 1, 0, -1):
            pass
            if queue.get(i).requester == member:
                removed.append(queue.remove(i))

        embed = Utils.get_embed(interaction, title=f'Removed {len(removed)} song{"" if len(removed) == 1 else "s"} queued by user {member.mention}.')
        for index in range(len(removed)):
            if index == 24:
                embed.add_field(name='And more...', value='...', inline=False)
                break
            embed.add_field(name=removed[index].uploader, value=removed[index].title, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="removeduplicates", description="Removes duplicate songs from the queue")
    async def remove_dupes(self, interaction: discord.Interaction):
        if not await Utils.Pretests.player_exists(interaction):
            return
        if not Utils.Pretests.has_discretionary_authority(interaction):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        player = Servers.get_player(interaction.guild_id)
        queue = player.queue

        #O(n) algorithm using a hash table
        table = {player.song.id : player.song} if player.song else {}
        removed = []
        i = 0
        while i < len(queue.get()):
            song = queue.get(i)
            if table.get(song.id) == None:
                table.update({song.id : song})
                i += 1
                continue
            removed.append(queue.remove(i))
        
        embed = Utils.get_embed(interaction, title=f'Removed {len(removed)} duplicate song{"" if len(removed) == 1 else "s"}.')
        for index in range(len(removed)):
            if index == 24:
                embed.add_field(name='And more...', value='...', inline=False)
                break
            embed.add_field(name=removed[index].uploader, value=removed[index].title, inline=False)
        await interaction.response.send_message(embed=embed)

    async def clear(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.player_exists(interaction):
            return
        
        if not Utils.Pretests.has_discretionary_authority(interaction):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return

        Servers.get_player(interaction.guild_id).queue.clear()
        await interaction.response.send_message('💥 Queue cleared')

    @app_commands.command(name="inspect", description="Inspects a song by number in queue")
    async def inspect(self, interaction: discord.Interaction, number_in_queue: int):
        if not await Utils.Pretests.player_exists(interaction):
            return
        
        # Convert to non-human-readable only if it's positive
        if number_in_queue > 0:
            # In this scenario 0 or 1 will mean the top song in queue
            number_in_queue -= 1
        song = Servers.get_player(interaction.guild_id).queue.get(number_in_queue)

        if song is None:
            await Utils.send(interaction, "Queue index does not exist.")
            return
        
        embed = Utils.get_embed(interaction, 
                                title=f'Inspecting song #{number_in_queue + 1}:',
                                url=song.original_url,
                                content=f'{song.title} -- {song.uploader}',
                                color=Utils.get_random_hex(song.id)
                                )
        embed.add_field(name='Duration:', value=song.parse_duration(song.duration), inline=True)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.set_image(url=song.thumbnail)
        embed.set_author(name=song.requester.display_name,
                        icon_url=song.requester.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="move", description="Moves a song in the queue to a different position. run queue command before using this command.")
    async def move(self, interaction: discord.Interaction, song_number: int, new_position: int) -> None:
        # Convert to non-human-readable
        song_number -= 1
        new_position -= 1
        if not await Utils.Pretests.playing_audio(interaction):
            return
        player = Servers.get_player(interaction.guild_id)
        if not Utils.Pretests.has_song_authority(interaction, player.queue.get(song_number)):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command or to modify this song.  Please refer to /help for more information.")
            return
        if (song_number < 0 or song_number > len(player.queue) - 1):
            await Utils.send(interaction, title='Invalid song number!', 
                            content="Please enter a valid song number.")
            return
        if (new_position < 0 and not new_position == -1):
            await Utils.send(interaction, title='Invalid position!', 
                            content="Please enter a valid position.")
            return
        
        if (new_position > len(player.queue) - 1):
            new_position = len(player.queue) - 1
            
        song = player.queue.pop(song_number)
        player.queue.add_at(song, new_position)

        if (new_position == -1):
            new_position = len(player.queue) - 1
        
        await Utils.send(interaction, title=f'Moved song {song_number + 1} to position {new_position + 1}')



async def setup(bot):
    Utils.pront("Cog QueueManagement loading...")
    await bot.add_cog(QueueManagement(bot))
    Utils.pront("Cog QueueManagement loaded!")