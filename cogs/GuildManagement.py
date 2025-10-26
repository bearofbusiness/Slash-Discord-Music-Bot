import discord
from discord.ext import commands
from discord import app_commands

import Utils
from Servers import Servers
from DB import DB
import Buttons


class GuildManagement(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="join", description="Adds the MaBalls to the voice channel you are in")
    async def _join(self, interaction: discord.Interaction) -> None:
        # checks if correct permissions are set
        perm_check = await Utils.Pretests.check_perms(interaction)
        if perm_check is not None:
            await interaction.response.send_message(f"My install link was not set up correctly, I am missing: {perm_check}")
            return

        if interaction.user.voice is None:  # checks if the user is in a voice channel
            await interaction.response.send_message('You are not in a voice channel', ephemeral=True)
            return

        if interaction.guild.voice_client is not None:  # checks if the bot is in a voice channel
            await interaction.response.send_message('I am already in a voice channel', ephemeral=True)
            return

        # Connect to the voice channel
        await interaction.user.voice.channel.connect(self_deaf=True)
        await Utils.send(interaction, title='Joined!', content=':white_check_mark:', progress=False)


    @app_commands.command(name="leave", description="Removes the MaBalls from the voice channel you are in")
    async def _leave(self, interaction: discord.Interaction) -> None:
        if not Utils.Pretests.has_discretionary_authority(interaction):
            await Utils.send(interaction, title='Insufficient permissions!', 
                        content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        if not await Utils.Pretests.voice_channel(interaction):
            return
        player = Servers.get_player(interaction.guild_id)
        # Clean up if needed
        if player is not None:
            if not Utils.Pretests.has_discretionary_authority(interaction):
                    await Utils.send(interaction, title='Insufficient permissions!', 
                                content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
                    return
            await Servers.get_player(interaction.guild_id).clean()
        # Otherwise, just leave VC
        else:
            await interaction.guild.voice_client.disconnect()
        await Utils.send(interaction, title='Left!', content=':white_check_mark:', progress=False)


    @app_commands.command(name="settings", description="Get or set the bot's settings for your server")
    async def _settings(self, interaction: discord.Interaction) -> None:
        for role in interaction.user.roles:
            if role.permissions.manage_channels or role.permissions.administrator: 
                embed = Utils.get_embed(interaction, title='Settings')
                embed.add_field(name='Now Playing Location', value=f"Changes where auto Now Playing messages are sent between VC and the channel the song was queued from. The current value is: `{('Text', 'VC')[DB.GuildSettings.get(interaction.guild_id, 'np_sent_to_vc')]}`")
                embed.add_field(name='Verbose Control Buttons', value=f"Adds verbose text to the control buttons on the auto Now Playing. The current value is: `{bool(DB.GuildSettings.get(interaction.guild_id, 'verbose_np'))}`")
                embed.add_field(name='Remove Orphaned Songs', value=f"Whether the bot should remove all the songs a user queued when they leave the VC. The current value is: `{bool(DB.GuildSettings.get(interaction.guild_id, 'remove_orphaned_songs'))}`")
                embed.add_field(name='Allow Playlist', value=f"Whether the bot should allow users to queue playlists. The current value is: `{('No', 'Yes', 'DJ Only')[DB.GuildSettings.get(interaction.guild_id, 'allow_playlist')]}`")
                embed.add_field(name='Leave Song Breadcrumbs', value=f"Whether the bot should leave breadcrumbs to previously played songs to be able trace back the queue. The current value is: `{bool(DB.GuildSettings.get(interaction.guild_id, 'song_breadcrumbs'))}`")
                await interaction.response.send_message(ephemeral=True, embed=embed, view=Buttons.GuildSettingsView(interaction))
                return
        await Utils.send(interaction, title='Insufficient permissions!', ephemeral=True)


async def setup(bot):
    Utils.pront("Cog GuildManagement loading...")
    await bot.add_cog(GuildManagement(bot))
    Utils.pront("Cog GuildManagement loaded!")