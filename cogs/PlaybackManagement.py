import discord
from discord.ext import commands


import Utils
from Servers import Servers

class PlaybackManagement(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @discord.slash_command(name="skip", description="Skips the currently playing song")
    async def _skip(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.playing_audio(ctx):
            return

        player = Servers.get_player(ctx.guild_id)

        await Utils.skip_logic(player, ctx)

    @discord.slash_command(name="force-skip", description="Skips the currently playing song without having a vote. (Requires Manage Channels permission.)")
    async def _force_skip(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.playing_audio(ctx):
            return

        # If there's enough users in vc for it to make sense check perms
        if len(Servers.get_player(ctx.guild_id).vc.channel.members) > 3:
            # Check song authority
            if not Utils.Pretests.has_song_authority(ctx, Servers.get_player(ctx.guild_id).song):
                await Utils.send(ctx, title='Insufficient permissions!', 
                                content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
                return
            
        Servers.get_player(ctx.guild_id).vc.stop()
        await Utils.send(ctx, "Skipped!", ":white_check_mark:")

    @discord.slash_command(name="replay", description="Restarts the current song")
    async def _replay(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.playing_audio(ctx):
            return
        
        player = Servers.get_player(ctx.guild_id)

        if not Utils.Pretests.has_song_authority(ctx, player.song):
            await Utils.send(ctx, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        
        player = Servers.get_player(ctx.guild_id)
        # Just add it to the top of the queue and skip to it
        # Dirty, but it works.
        player.queue.add_at(player.song, 0)
        player.vc.stop()
        await Utils.send(ctx, title='⏪ Rewound')

    @discord.slash_command(name="pause", description="Pauses the current song")
    async def _pause(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.playing_audio(ctx):
            return
        Servers.get_player(ctx.guild_id).pause()
        await Utils.send(ctx, title='⏸ Paused')

    @discord.slash_command(name="resume", description="Resumes the current song")
    async def _resume(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.playing_audio(ctx):
            return
        Servers.get_player(ctx.guild_id).resume()
        await Utils.send(ctx, title='▶ Resumed')



def setup(bot: discord.Bot):
    Utils.pront("Cog PlaybackManagement loading...")
    bot.add_cog(PlaybackManagement(bot))
    Utils.pront("Cog PlaybackManagement loaded!")