import discord
from discord.ext import commands

class Commands(commands.Cog):
    def _init__(self,bot):
        self.bot= bot



    @commands.command()
    async def ping(self, ctx):
        """Check the bot latency"""
        embed = discord.Embed(
            description=f" :ping_pong:  **|** Pong! I have a bot ping of: **{round(self.bot.latency * 1000)}ms**",
            colour=discord.Colour.blue(),
        )
        embed.set_footer(text="It's your turn now!")

        await ctx.send(embed=embed)











def setup(bot):
    bot.add_cog(Commands(bot))