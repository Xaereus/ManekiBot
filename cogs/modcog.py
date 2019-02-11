from discord.ext import commands
import discord


class ModCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, mbr: discord.Member):
        if mbr == ctx.author:
            await ctx.send("You can't kick yourself!")
        elif mbr == ctx.bot.user:
            await ctx.send("I'm not gonna kick myself...")
        elif ctx.author.top_role.position < mbr.top_role.position:
            await ctx.send("They have more authority than you, so I can't kick them.")
        else:
            try:
                await mbr.kick()
                await ctx.send(f"{mbr.mention} was kicked from {ctx.guild.name}")
            except discord.errors.Forbidden:
                await ctx.send(f"I'm not allowed to kick.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, mbr: discord.Member):
        if mbr == ctx.author:
            await ctx.send("You can't ban yourself!")
        elif mbr == ctx.bot.user:
            await ctx.send("I'm not gonna ban myself...")
        elif ctx.author.top_role.position < mbr.top_role.position:
            await ctx.send("They have more authority than you, so I can't ban them.")
        else:
            try:
                await mbr.ban()
                await ctx.send(f"{mbr.mention} was banned from {ctx.guild.name}")
            except discord.errors.Forbidden:
                await ctx.send(f"I'm not allowed to ban.")


def setup(bot):
    bot.add_cog(ModCog(bot))
