import random
import json
import discord
import aiohttp
from discord.ext import commands


class CuteCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, *, member: discord.Member = None):
        """Hug someone on the server <3"""
        embed = discord.Embed(title = "Command: hug", color = 0xFFC0CB)
        session = aiohttp.ClientSession()
        response = await session.get(
            'http://api.giphy.com/v1/gifs/search?q=hug+manga&api_key=NLUaerigtVW04pj4P4slXZOexvpC5VN3&limit=10')
        gif_choice = random.randint(0, 9)
        data = json.loads(await response.text())
        embed.set_image(url = data['data'][gif_choice]['images']['original']['url'])

        if member is None:
            embed.description = f"{ctx.message.author.mention} has been hugged!"
        else:
            if member.id == ctx.message.author.id:
                embed.description = f"{ctx.message.author.mention} has hugged themself!"
            elif member.id == self.bot.user.id:
                embed.description = f"I got a hug from {ctx.message.author.mention}! <3"
            else:
                embed.description = f"{member.mention} has been hugged by {ctx.message.author.mention}!"

        await session.close()

        await ctx.send(embed = embed)

    @commands.command()
    async def wave(self, ctx):
        embed = discord.Embed(color = 0xFFC0CB)
        session = aiohttp.ClientSession()
        response = await session.get(
            'http://api.giphy.com/v1/gifs/search?q=kawaii+wave&api_key=NLUaerigtVW04pj4P4slXZOexvpC5VN3&limit=1')
        data = json.loads(await response.text())
        embed.set_image(url = data['data'][0]['images']['original']['url'])
        await session.close()

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(CuteCog(bot))
