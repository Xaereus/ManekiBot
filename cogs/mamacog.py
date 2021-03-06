import discord
from discord.ext import commands
from .utils.settings import settings
from .utils import checks


class MamaCog:
    def __init__(self, bot):
        self.bot = bot

    @checks.is_guardian()
    @commands.command(name = 'changePlaying', aliases = ['playing'])
    async def change_playing(self, ctx, *game):
        if ctx.message.author.id in settings.guardians:
            game = ' '.join(game)
            settings.bot_settings['currActivity'] = game
            settings.save_bot_settings()
            await self.bot.change_presence(activity = discord.Game(name = game))
        else:
            await ctx.send("No!")


def setup(bot):
    bot.add_cog(MamaCog(bot))
