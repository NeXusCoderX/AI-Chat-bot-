import discord
from discord.ext import commands
import aiohttp
import io
import gtts

class UserCommands(commands.Cog):
    """General user commands"""
    cog_info = {
        "name": "User",
        "emoji": "\N{BUST IN SILHOUETTE}",
        "color": discord.Color.blue()
    }
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["av"])
    async def avatar(self, ctx: commands.Context, *, member: discord.Member = None):
        """View your avatar
        
        Arguments:
            member (a user ID or mention, optional): The member to tag
        Examples:
            {prefix}avatar
            {prefix}avatar @beep
        """
        if not member:
            member = ctx.message.author

        emb = discord.Embed(
            color=member.color,
            timestamp=ctx.message.created_at
        )

        emb.set_author(name=f"Avatar of {member}")
        emb.set_image(url=member.display_avatar.url)
        emb.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=emb)





def setup(bot: commands.Bot):
    bot.add_cog(UserCommands(bot))