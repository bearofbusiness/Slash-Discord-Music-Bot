import discord
import math

# Imports from our files
# Import Player rather than from Player to resolve a circular import
import Player
import Utils
from Servers import Servers
from Song import Song

class NowPlayingButtons(discord.ui.View):
    def __init__(self, player: Player):
        super().__init__(timeout=None)
        self.player = player

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏪")
    async def rewind_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.queue.add_at(self.player.song, 0)
        self.player.vc.stop()
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title="⏪ Rewound"))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏸")
    async def pause_play_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.player.vc.is_paused():
            self.player.vc.resume()
            self.player.song.resume()
            button.emoji = "⏸"
            self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
            await interaction.response.send_message(embed=Utils.get_embed(interaction, title="▶ Resumed"))
            return
        self.player.vc.pause()
        self.player.song.pause()
        button.emoji = "▶"
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title="⏸ Paused"))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏩")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await Utils.skip_logic(self.player, interaction)

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔂")
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.set_loop(not self.player.looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='🔂 Looped.' if self.player.looping else 'Loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔁")
    async def queue_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.set_queue_loop(not self.player.queue_looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='🔁 Queue looped.' if self.player.queue_looping else 'Queue loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='♾')
    async def true_loop_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.set_true_loop(not self.player.true_looping)
        self.player.last_np_message = await self.player.last_np_message.edit(embed=Utils.get_now_playing_embed(self.player, progress=True), view=self)
        await interaction.response.send_message(ephemeral=True, embed=Utils.get_embed(interaction, title='♾ True looped.' if self.player.true_looping else 'True loop disabled.'))

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="🔀")
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.player.queue.shuffle()
        await interaction.response.send_message(embed=Utils.get_embed(interaction, title='🔀 Queue shuffled'))


    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏺")
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

