from .settings import settings
from discord.ext import commands


def check_is_guardian(ctx):
    return ctx.message.author.id in settings.guardians


def is_guardian():
    return commands.check(check_is_guardian)
