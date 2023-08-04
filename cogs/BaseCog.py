import discord
from discord.ext import commands
from discord import app_commands

import Utils

class BaseCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="sample_command", description="this should not be loaded")
    async def _sample_command(self, interaction: discord.Interaction) -> None:
        interaction.response.send_message("the")

async def setup(bot):
    Utils.pront("Cog BaseCog loading...")
    await bot.add_cog(BaseCog(bot))
    Utils.pront("Cog BaseCog loaded!")