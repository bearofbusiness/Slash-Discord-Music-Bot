import discord
from discord.ext import commands


import Utils
from Servers import Servers

class PlayerManagement(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @discord.slash_command(name="now", description="Shows the current song")
    async def _now(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.player_exists(ctx):
            return
        await ctx.response.send_message(embed=Utils.get_now_playing_embed(Servers.get_player(ctx.guild_id), progress=True))

    loop = discord.SlashCommandGroup(name='loop', description='Commands that relate to the post-playback behavior of songs')

    @loop.command(name="single", description="Loops the current song")
    async def _loop(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.player_exists(ctx):
            return
        player = Servers.get_player(ctx.guild.id)
        player.set_loop(not player.looping)
        await Utils.send(ctx, title='🔂 Looped.' if player.looping else 'Loop disabled.')

    @loop.command(name="queue", description="Loops the queue")
    async def _queue_loop(self, ctx: discord.ApplicationContext) -> None:
        if not await Utils.Pretests.player_exists(ctx):
            return
        player = Servers.get_player(ctx.guild.id)
        player.set_queue_loop(not player.queue_looping)
        await Utils.send(ctx, title='🔁 Queue looped.' if player.queue_looping else 'Queue loop disabled.')

    @loop.command(name="true", description="Loops and adds songs to a random position in queue")
    async def _true_loop(self, ctx: discord.ApplicationContext) -> None:
        player = Servers.get_player(ctx.guild.id)
        player.set_true_loop(not player.queue_looping)
        await Utils.send(ctx, title='♾ True looped.' if player.true_looping else 'True loop disabled.')

    @discord.slash_command(name='force-reset-player', description="Did something go wrong while listening?  Run this command and it will (hopefully) sort it out!")
    async def _force_reset_player(self, ctx: discord.ApplicationContext):
        if not await Utils.Pretests.player_exists(ctx):
            return
        player = Servers.get_player(ctx.guild_id)
        await Utils.force_reset_player(player)
        

def setup(bot: discord.Bot):
    Utils.pront("Cog PlayerManagement loading...")
    bot.add_cog(PlayerManagement(bot))
    Utils.pront("Cog PlayerManagement loaded!")
