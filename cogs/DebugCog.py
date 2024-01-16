import discord
import io
import sys
from discord.ext import commands

import Utils
from Servers import Servers

class DebugCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.hybrid_command(name="unload", description="unloads the debug cog")
    async def _unload(self, ctx: commands.Context) -> None:
        await self.bot.remove_cog("DebugCog")
        await Utils.send(ctx, 'done')
        await self.bot.tree.sync()
        
    @commands.hybrid_command(name="eval", description="debug cog")
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, command: str) -> None:
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
        await Utils.send(ctx, title='Command Sent:', description='in:\n```' + command + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')


    @commands.hybrid_command(name="exec", description="debug cog")
    @commands.is_owner()
    async def _exec(self, ctx: commands.Context, command: str) -> None:
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
        await Utils.send(ctx, title='Command Sent:', description='in:\n```' + command + '```' + '\n\nout:```ansi\n' + str(mystdout.getvalue()) + '```')


    @commands.hybrid_group(name='list')
    async def list_group(self, ctx: commands.Context):
        pass

    @list_group.command(name='lss', description='lists hashes')
    @commands.is_owner()
    async def _list_servers(self, ctx: commands.Context) -> None:
        stringBuilder = ""
        for i in self.bot.guilds:
            stringBuilder += str(i.name) + "\n"

        await Utils.send(ctx, title='Hashes:', description=stringBuilder)


async def setup(bot):
    Utils.pront("Cog DebugCog loading...")
    await bot.add_cog(DebugCog(bot))
    Utils.pront("Cog DebugCog loaded!")