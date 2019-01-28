import os
import sys
import platform
import time
import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
from cogs.utils.settings import settings


class Maneki(commands.Bot):
    """
    Framework for a bot, designed to be used with cogs and not as a stand-alone.
    Will eventually be converted to use the AutoShardedBot class instead of Bot.
    """

    def __init__(self, *args, **kwargs):
        self.logger = set_logger()

        super().__init__(*args, activity = discord.Game(name = settings.current_activity),
                         command_prefix = "!!", **kwargs)

    # Bot startup output
    async def on_ready(self):
        print(f"{time.ctime()} :: Booted as {self.user.name} (ID - {self.user.id})")
        print(f"Playing game: {settings.current_activity}\n")
        print("Connected guilds:\n" + '\n'.join([f"\t{guild.id} > {guild.name}" for guild in self.guilds]))
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})\n\n")

    def load_cogs(self):
        print("Loading cogs...")
        for cog in settings.loaded_extensions:
            print(f"\tLoading {cog}...")
            try:
                self.load_extension(f"cogs.{cog}")
                print(f"\t{cog} loaded.")
            except (discord.ClientException, ImportError) as e:
                print(f"\tFailed to load {cog} || {type(e)}: {e}")
                settings.disable_extension(cog)
                print(f"\tDisabling {cog}.")
        print("Cogs loaded.\n")

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await ctx.send(page)
        else:
            pages = self.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)


def set_logger():
    # TODO: optimize loggers for Maneki
    logger = logging.getLogger("maneki")
    logger.setLevel(logging.INFO)

    neki_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt = "[%Y-%m-%d:%H:%M]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(neki_format)
    stdout_handler.setLevel(logging.INFO)

    fhandler = RotatingFileHandler(
        filename = 'data/logs/maneki.log', encoding = 'utf-8', mode = 'a',
        maxBytes = 10 ** 7, backupCount = 3)
    fhandler.setFormatter(neki_format)

    logger.addHandler(fhandler)
    logger.addHandler(stdout_handler)

    dpy_logger = logging.getLogger("discord")
    dpy_logger.setLevel(logging.WARNING)

    handler = logging.FileHandler(
        filename = 'data/logs/discord.log', encoding = 'utf-8', mode = 'a')
    handler.setFormatter(neki_format)
    dpy_logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    bot = Maneki()
    if settings.loaded_extensions != {}:
        bot.load_cogs()
    else:
        print("Running without cogs.")

    bot.run(settings.token, reconnect = True)
