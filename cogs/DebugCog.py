import discord
import io
import sys
from discord.ext import commands
import discord
from discord.ext import commands
from discord import app_commands

import Utils
from Servers import Servers

class DebugCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(name="unload", description="unloads the debug cog")
    async def _unload(self, interaction: discord.Interaction) -> None:
        await self.bot.remove_cog("DebugCog")
        await Utils.send(ctx, 'done')
        await self.bot.tree.sync()
        
    @app_commands.command(name="eval", description="debug cog")
    @commands.is_owner()
    async def _eval(self, interaction: discord.Interaction, command: str) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        command.rstrip("`")
        command.lstrip("`")
        command.lstrip("python")
        try:
            print(eval(command))
        except Exception as e:
            Utils.pront(e, "ERROR")
        sys.stdout = old_stdout
        print(mystdout.getvalue())
        await Utils.send(ctx, title='Command Sent:', content='in:\n```' + command + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')


    @app_commands.command(name="exec", description="debug cog")
    @commands.is_owner()
    async def _exec(self, interaction: discord.Interaction, command: str) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        command.rstrip("`")
        command.lstrip("`")
        command.lstrip("python")

        try:
            exec(command)
        except Exception as e:
            Utils.pront(e, "ERROR")
        sys.stdout = old_stdout
        print(mystdout.getvalue())
        await Utils.send(ctx, title='Command Sent:', content='in:\n```' + command + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')

    async def _list_servers(self) -> None:
        stringBuilder = ""
        for i in self.bot.guilds:
            stringBuilder += str(i.name) + "\n"
        print(stringBuilder)



async def setup(bot):
    Utils.pront("Cog DebugCog loading...")
    await bot.add_cog(DebugCog(bot))
    Utils.pront("Cog DebugCog loaded!")