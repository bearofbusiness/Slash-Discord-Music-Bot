import discord
import math

# Imports from our files
# Import Player rather than from Player to resolve a circular import
import Player
import Utils
from DB import DB
from Servers import Servers
from Song import Song
from Pages import Pages

class NowPlayingButtons(discord.ui.View):
    def __init__(self, player: Player):
        super().__init__(timeout=None)
        self.player = player

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏪", row=1)
    async def rewind_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None: 
        if not await Utils.Pretests.playing_audio(interaction):
            return
        
        if not Utils.Pretests.has_song_authority(interaction, self.player.song):
            await Utils.send(interaction, title='Insufficient permissions!', 
                            content="You don't have the correct permissions to use this command!  Please refer to /help for more information.", ephemeral=True)
            return
        
        self.player.queue.add_at(self.player.song, 0)
        self.player.vc.stop()
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title="⏪ Rewound"))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏸", row=1)
    async def pause_play_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return
        if self.player.vc.is_paused():
            self.player.resume()
            button.emoji = "⏸"
            self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
            await interaction.response.send_message(embed=Utils.get_embed(interaction, title="▶ Resumed"))
            return
        self.player.pause()
        button.emoji = "▶"
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title="⏸ Paused"))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏩", row=1)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.playing_audio(interaction):
            return
        await Utils.skip_logic(self.player, interaction)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔂", row=2)
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.voice_channel(interaction):
            return
        self.player.set_loop(not self.player.looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='🔂 Looped.' if self.player.looping else 'Loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔁", row=2)
    async def queue_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.voice_channel(interaction):
            return
        self.player.set_queue_loop(not self.player.queue_looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='🔁 Queue looped.' if self.player.queue_looping else 'Queue loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='♾', row=2)
    async def true_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.voice_channel(interaction):
            return
        self.player.set_true_loop(not self.player.true_looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='♾ True looped.' if self.player.true_looping else 'True loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔀", row=3)
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if not await Utils.Pretests.voice_channel(interaction):
            return
        player = Servers.get_player(interaction.guild_id)
        if not Utils.Pretests.has_discretionary_authority(interaction):
            await Utils.send(interaction, title='Insufficient permissions!', 
                        content="You don't have the correct permissions to use this command!  Please refer to /help for more information.")
            return
        player.queue.shuffle()
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title='🔀 Queue shuffled'))


    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏺", row=3)
    async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(delete_after=1, ephemeral=True, embed=Utils.get_embed(interaction, '⏺ Refreshed', progress=False))

class SearchSelection(discord.ui.View):
    def __init__(self, query_result, *, timeout=180):
        self.query_result = query_result
        super().__init__(timeout=timeout)
    
    # All the buttons will call this method to add the song to queue
    async def __selector(self, index: int, interaction: discord.Interaction) -> None:
        entry = self.query_result.get('entries')[index]
        song = Song(interaction, entry.get('original_url'), entry)

        # If not in a VC, join
        if interaction.guild.voice_client is None:
            await interaction.user.voice.channel.connect(self_deaf=True)

        # If player does not exist, create one.
        if Servers.get_player(interaction.guild_id) is None:
            Servers.add(interaction.guild_id, Player.Player(
                interaction.guild.voice_client, song))
        # If it does, add the song to queue
        else:
            Servers.get_player(interaction.guild_id).queue.add(song)

        # Create embed to go along with it
        embed = Utils.get_embed(
            interaction,
            title=f'[{len(Servers.get_player(interaction.guild_id).queue.get())} Added to Queue:',
            url=song.original_url,
            color=Utils.get_random_hex(song.id)
        )
        embed.add_field(name=song.uploader, value=song.title, inline=False)
        embed.add_field(name='Requested by:', value=song.requester.mention)
        embed.add_field(name='Duration:',
                        value=Song.parse_duration(song.duration))
        embed.set_thumbnail(url=song.thumbnail)
        await interaction.response.send_message(embed=embed)


    @discord.ui.button(label="1",style=discord.ButtonStyle.blurple)
    async def button_one(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.__selector(0, interaction)

    @discord.ui.button(label="2",style=discord.ButtonStyle.blurple)
    async def button_two(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.__selector(1, interaction)

    @discord.ui.button(label="3",style=discord.ButtonStyle.blurple)
    async def button_three(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.__selector(2, interaction)

    @discord.ui.button(label="4",style=discord.ButtonStyle.blurple)
    async def button_four(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.__selector(3, interaction)

    @discord.ui.button(label="5",style=discord.ButtonStyle.blurple)
    async def button_five(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.__selector(4, interaction)

class QueueButtons(discord.ui.View):
    def __init__(self, *, timeout=180, page=1):
        self.page = page
        super().__init__(timeout=timeout)

    def get_queue_embed(self, interaction: discord.Interaction):
        player = Servers.get_player(interaction.guild_id)
        page_size = 5
        queue_len = len(player.queue)
        max_page = math.ceil(queue_len / page_size)

        if self.page < 0:
            self.page = max_page - 1
        elif self.page >= max_page:
            self.page = 0
        

        # The index to start reading from Queue
        min_queue_index = page_size * (self.page)
        # The index to stop reading from Queue
        max_queue_index = min_queue_index + page_size

        embed = Utils.get_embed(interaction, title='Queue', color=Utils.get_random_hex(
            player.song.id), progress=False)

        # Loop through the region of songs in this page
        for i in range(min_queue_index, max_queue_index):
            if i >= queue_len:
                break
            song = player.queue.get()[i]

            embed.add_field(name=f"`{i + 1}`: {song.title}",
                            value=f"by {song.uploader}\nAdded By: {song.requester.mention}", inline=False)

        embed.set_footer(
            text=f"Page {self.page + 1}/{max_page} | {queue_len} song{'s' if queue_len != 1 else ''} in queue")
        return embed

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⬅")
    async def button_left(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.page -= 1
        await interaction.response.edit_message(embed=self.get_queue_embed(interaction), view=self)
        
    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="➡")
    async def button_right(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.page += 1
        await interaction.response.edit_message(embed=self.get_queue_embed(interaction), view=self)


class GuildSettingsView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=180)

    @discord.ui.select(options=[
            discord.SelectOption(label='Now Playing location', value='np_sent_to_vc', description='Changes where auto Now Playing messages are sent.'),
            discord.SelectOption(label='Remove Orphaned Songs', value='remove_orphaned_songs', description='Removes all the songs a user queued when they leave the VC.'),
            discord.SelectOption(label='Allow Playlist', value='allow_playlist', description='Whether the bot should allow users to queue playlists.')
        ], placeholder='Select a setting to edit.', )
    async def setting_selection(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Remove any existing Buttons before spawning a new one
        item = self.children[0]
        self.clear_items().add_item(item)

        # Get current state from DB
        value = select.values[0]
        current_state = DB.GuildSettings.get(interaction.guild_id, value)

        # Define the messages for the ToggleButton
        match value:
            case 'np_sent_to_vc':
                select.placeholder = "Now Playing Location"
                self.add_item(ToggleButton(current_state, value, ['Text', 'VC']))
            case 'remove_orphaned_songs':
                select.placeholder = "Remove Orphaned Songs"
                self.add_item(ToggleButton(current_state, value))
            case 'allow_playlist':
                select.placeholder = "Allow Playlist"
                self.add_item(TripleButton(current_state, value))
            case default:
                raise NotImplementedError(f"We is boned... returned '{default}' in GuildSettingsView selection")
            
        await interaction.response.edit_message(view=self)

class ToggleButton(discord.ui.Button):
    def __init__(self, state: bool, value: str, messages: list[str] = ['False', 'True']):
        self.value = value
        self.state = state
        self.messages = messages
        style = discord.ButtonStyle.green if state else discord.ButtonStyle.red
        super().__init__(style=style, label=messages[state])

    async def callback(self, interaction: discord.Interaction):
        self.state = not self.state
        self.style = discord.ButtonStyle.green if self.state else discord.ButtonStyle.red
        self.label = self.messages[self.state]
        await self.update(interaction)

    async def update(self, interaction: discord.Interaction):
        DB.GuildSettings.set(interaction.guild_id, self.value, self.state)
        await interaction.response.edit_message(view=self.view.remove_item(self).add_item(self))

class TripleButton(ToggleButton):
    def __init__(self, state: int, value: str, messages: list[str] = ['False', 'True', 'DJ Only']):
        self.styles = [discord.ButtonStyle.red, discord.ButtonStyle.green, discord.ButtonStyle.blurple]
        super().__init__(False, value, messages)
        self.state = state
        self.style = self.styles[state]
        self.label = self.messages[state]

    async def callback(self, interaction: discord.Interaction):
        self.state = (self.state + 1) % 3
        self.style = self.styles[self.state]
        self.label = self.messages[self.state]

        await super().update(interaction)


class HelpView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=300)

    @discord.ui.select(options=[
            discord.SelectOption(label='General Help', description='General tips and tricks for using MaBalls'),
            discord.SelectOption(label='Adding Songs', description='Commands for adding one or many songs to the queue'),
            discord.SelectOption(label='Removing Songs', description='Commands for removing one or many songs from the queue'),
            discord.SelectOption(label='Queue Management', description='Commands for modifying the queue'),
            discord.SelectOption(label='Other Commands', description='Miscellaneous commands that don\'t fit into to any category')
        ], placeholder='Select a command category.', )
    async def setting_selection(self, interaction: discord.Interaction, select: discord.ui.Select):
        value = select.values[0]
        self.placeholder = value

        # Remove any existing Buttons before spawning a new one
        item = self.children[0]
        self.clear_items().add_item(item)

        category = Pages.get_category(value)
        style = category.get('cat_style')
        for item in category.get('buttons'):
            self.add_item(HelpButton(item, style))
        
        embed = discord.Embed.from_dict(category.get('page'))
        await interaction.response.edit_message(embed=embed, view=self)


class HelpButton(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed.from_dict(Pages.get_command_page(self.label))
        await interaction.response.edit_message(embed=embed, view=self.view)
