import discord
from discord.ext import commands
from discord import app_commands

import Utils
from Servers import Servers

class PlaybackManagement(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="skip", description="Skips the currently playing song")
    async def skip(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return

        player = Servers.get_player(interaction.guild_id)

        await Utils.skip_logic(player, interaction)


    @app_commands.command(name="forceskip", description="Skips the currently playing song without having a vote. (Requires Manage Channels permission.)")
    async def force_skip(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return

        # If there's enough users in vc for it to make sense check perms
        if len(Servers.get_player(interaction.guild_id).vc.channel.members) > 3:
            # Check song authority
            if not Utils.Pretests.has_song_authority(interaction, Servers.get_player(interaction.guild_id).song):
                await Utils.send(interaction, title='Insufficient permissions!', 
                                content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
                return
            
        Servers.get_player(interaction.guild_id).vc.stop()
        await Utils.send(interaction, "Skipped!", ":white_check_mark:")

    @app_commands.command(name="replay", description="Restarts the current song")
    async def replay(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return
        
        player = Servers.get_player(interaction.guild_id)

        if not Utils.Pretests.has_song_authority(interaction, player.song):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        
        player = Servers.get_player(interaction.guild_id)
        # Just add it to the top of the queue and skip to it
        # Dirty, but it works.
        player.queue.add_at(player.song, 0)
        player.vc.stop()
        await Utils.send(interaction, title='⏪ Rewound')


    @app_commands.command(name="pause", description="Pauses the current song")
    async def pause(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return
        Servers.get_player(interaction.guild_id).pause()
        await Utils.send(interaction, title='⏸ Paused')


    @app_commands.command(name="resume", description="Resumes the current song")
    async def resume(self, interaction: discord.Interaction) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return
        Servers.get_player(interaction.guild_id).resume()
        await Utils.send(interaction, title='▶ Resumed')

async def setup(bot):
    Utils.pront("Cog PlaybackManagement loading...")
    await bot.add_cog(PlaybackManagement(bot))
    Utils.pront("Cog PlaybackManagement loaded!")