import os
import subprocess

import discord
import dotenv
from discord.ext import commands
from discord import app_commands

import Utils

class Update(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @app_commands.command(
        name="update",
        description="Update YT-DLP to the latest nightly channel",
    )
    async def _update(self, interaction: discord.Interaction):
        """
            This command REQUIRES python pip, tmux and a venv, this command also only works after all required packages
            have already been installed and the bot needs to be running in a tmux session.
            This simply updates those existing packages and forces yt-dlp to be on the latest nightly version.
            When this command is run, it will create a list of existing packages already installed in the venv and update all of them,
            it will then force reinstall YT-DLP (**using pip**) to be on the latest version from the nightly channel.
            This also REQUIRES linux to run properly.
        """

        if not self.has_update_authority(interaction):
            await Utils.send(interaction,
                title='Insufficient permissions!',
                content="You don't have the correct permissions to use this command!  Please refer to /help for more information."
            )
            return

        await interaction.response.defer(thinking=True)

        # Paths and names
        TMUX_SESSION_NAME = "SlashDiscordMusicBot"
        BOT_DIR = os.getcwd()
        VENV_PYTHON = f"{BOT_DIR}/.venv/bin/python"
        YT_DLP_NEW_VERSION = ""

        try:
            # Get current tmux session name for deletion later
            TMUX_OLD = subprocess.run(
                ["tmux", "display-message", "-p", "#S"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # Run pip upgrade inside venv for all venv packages and update yt-dlp to nightly
            p1 = subprocess.run([
                "python", "-m", "pip", "install", "--upgrade", "pip"
            ], check=True)

            while p1.returncode is not None:
                if p1.returncode == 0:
                    await interaction.followup.send("Finished pip update.")
                    break

            subprocess.run([
                "touch", f"{BOT_DIR}/packages.txt"
            ], check=True)

            subprocess.run("pip freeze | cut -d '=' -f 1 | sort -u > packages.txt", shell=True, check=True)

            p2 = subprocess.run([
                "pip", "install", "--upgrade", "-r", "packages.txt"
            ], check=True)

            while p2.returncode is not None:
                if p2.returncode == 0:
                    await interaction.channel.send("Finished venv packages update.")
                    break

            p3 = subprocess.run([
                f"{VENV_PYTHON}", "-m", "pip", "install", "--upgrade", "--force-reinstall",
                "git+https://github.com/yt-dlp/yt-dlp.git"
            ], check=True)

            YT_DLP_NEW_VERSION = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            while p3.returncode is not None:
                if p3.returncode == 0:
                    await interaction.channel.send("Finished yt-dlp update to " + YT_DLP_NEW_VERSION + ".")
                    break

            TMUX_NEW = TMUX_SESSION_NAME + "-" + YT_DLP_NEW_VERSION

            # Create new tmux session and start the bot in it
            p4 = subprocess.run([
                "tmux", "new-session", "-d", "-s", TMUX_NEW,
                f"bash -c 'cd {BOT_DIR} && source .venv/bin/activate && python musS_D.py'"
            ], check=True)

            while p4.returncode is not None:
                if p4.returncode == 0:
                    await interaction.channel.send("Created new process.")

            await interaction.channel.send("Finished installing all packages.\nTerminating old process.")

            if TMUX_OLD:
                subprocess.run(["tmux", "kill-session", "-t", TMUX_OLD], check=False)

        except subprocess.CalledProcessError as e:
            print(e.stderr)
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def __has_update_authority(interaction: discord.Interaction) -> bool:
        """
        Checks if the interaction.user has discretionary authority in the current scenario.

        Parameters
        ----------
        interaction: `discord.Interaction`

        Returns
        -------
        bool
            Whether the interaction.user should have discretionary authority.
        """

        dotenv.load_dotenv()
        developers = list(os.environ.get('developers'))

        # for developers
        if interaction.user.id in developers:
            return True
        return False


async def setup(bot):
    Utils.pront("Cog Update loading...")
    await bot.add_cog(Update(bot))
    Utils.pront("Cog Update loaded!")