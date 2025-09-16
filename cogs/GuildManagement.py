import discord
from discord.ext import commands

import Utils
from Servers import Servers
from DB import DB
import Buttons

class GuildManagement(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="join", description="Adds the MaBalls to the voice channel you are in")
    async def _join(self, ctx: discord.ApplicationContext) -> None:
        if ctx.user.voice is None:  # checks if the user is in a voice channel
            await ctx.response.send_message('You are not in a voice channel', ephemeral=True)
            return
        if ctx.guild.voice_client is not None:  # checks if the bot is in a voice channel
            await ctx.response.send_message('I am already in a voice channel', ephemeral=True)
            return
        # Connect to the voice channel
        await ctx.user.voice.channel.connect(self_deaf=True)
        await Utils.send(ctx, title='Joined!', content=':white_check_mark:', progress=False)

    @discord.slash_command(name="leave", description="Removes the MaBalls from the voice channel you are in")
    async def _leave(self, ctx: discord.ApplicationContext) -> None:
        if not Utils.Pretests.has_discretionary_authority(ctx):
            await Utils.send(ctx, title='Insufficient permissions!', 
                        content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        if not await Utils.Pretests.voice_channel(ctx):
            return
        player = Servers.get_player(ctx.guild_id)
        # Clean up if needed
        if player is not None:
            if not Utils.Pretests.has_discretionary_authority(ctx):
                    await Utils.send(ctx, title='Insufficient permissions!', 
                                content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
                    return
            await Servers.get_player(ctx.guild_id).clean()
        # Otherwise, just leave VC
        else:
            await ctx.guild.voice_client.disconnect()
        await Utils.send(ctx, title='Left!', content=':white_check_mark:', progress=False)
        
    @discord.slash_command(name="settings", description="Get or set the bot's settings for your server")
    async def _settings(self, ctx: discord.ApplicationContext) -> None:
        for role in ctx.user.roles:
            if role.permissions.manage_channels or role.permissions.administrator: 
                embed = Utils.get_embed(ctx, title='Settings')
                embed.add_field(name='Now Playing Location', value=f"Changes where auto Now Playing messages are sent between VC and the channel the song was queued from. The current value is: `{('Text', 'VC')[DB.GuildSettings.get(ctx.guild_id, 'np_sent_to_vc')]}`")
                embed.add_field(name='Verbose Control Buttons', value=f"Adds verbose text to the control buttons on the auto Now Playing. The current value is: `{bool(DB.GuildSettings.get(ctx.guild_id, 'verbose_np'))}`")
                embed.add_field(name='Remove Orphaned Songs', value=f"Whether the bot should remove all the songs a user queued when they leave the VC. The current value is: `{bool(DB.GuildSettings.get(ctx.guild_id, 'remove_orphaned_songs'))}`")
                embed.add_field(name='Allow Playlist', value=f"Whether the bot should allow users to queue playlists. The current value is: `{('No', 'Yes', 'DJ Only')[DB.GuildSettings.get(ctx.guild_id, 'allow_playlist')]}`")
                embed.add_field(name='Leave Song Breadcrumbs', value=f"Whether the bot should leave breadcrumbs to previously played songs to be able trace back the queue. The current value is: `{bool(DB.GuildSettings.get(ctx.guild_id, 'song_breadcrumbs'))}`")
                await ctx.response.send_message(ephemeral=True, embed=embed, view=Buttons.GuildSettingsView(ctx))
                return
        await Utils.send(ctx, title='Insufficient permissions!', ephemeral=True)

def setup(bot: discord.Bot):
    Utils.pront("Cog GuildManagement loading...")
    bot.add_cog(GuildManagement(bot))
    Utils.pront("Cog GuildManagement loaded!")