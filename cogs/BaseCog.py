import discord
from discord.ext import commands


import Utils

class BaseCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @discord.slash_command(name="sample_command", description="this should not be loaded")
    async def _sample_command(self, ctx: discord.ApplicationContext) -> None:
        ctx.response.send_message("the")

def setup(bot: discord.Bot):
    Utils.pront("Cog BaseCog loading...")
    bot.add_cog(BaseCog(bot))
    Utils.pront("Cog BaseCog loaded!")