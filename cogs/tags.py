import discord
from discord.ext import commands

import asyncio

class TagsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_tag(self, guild_id, tag_name):
        cursor = await self.bot.db.fetch(
            "SELECT * FROM taggingData "
            "WHERE guild_id = $1 AND tag_name = $2", guild_id, tag_name)

        if cursor:
            return dict(cursor[0])
        return

    async def can_edit_tag(self, ctx: commands.Context, tag):
        # -- If the user in the tag does not match the one in context
        if tag["user_added"] != ctx.author.id:
            # -- But the user in context has an specific role
            if ctx.author.get_role(914188064493043752):
                return True
            # -- Else
            return False
        # -- Else
        return True


    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag_name):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        
        if not tag:
            # Similarity query
            cursor = await self.bot.db.fetch(
                "SELECT tag_name, tag_name <-> $1 AS sml FROM taggingData "
                "WHERE guild_id = $2 AND tag_name % $1 "
                "ORDER BY sml DESC, tag_name;", 
                tag_name, ctx.guild.id
            )

            if cursor:
                return await ctx.send(f"No such tag exists. Did you mean ``{cursor[0]['tag_name']}``?")
            else:
                return await ctx.send("No such tag exists.")

        await ctx.send(tag["tag_text"])

        await self.bot.db.execute(
            "UPDATE taggingData SET uses = $1 "
            "WHERE guild_id = $2 AND user_added = $3 AND tag_name = $4", 
            (tag["uses"] or 0) + 1, ctx.guild.id, ctx.author.id, tag_name)

    @tag.command(name="create")
    async def create(self, ctx, tag_name, *, tag_text):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        if tag:
            return await ctx.send("A tag with such name already exists.")

        await self.bot.db.execute(
            "INSERT INTO taggingData (guild_id, user_added, tag_name, tag_text) "
            "VALUES ($1,$2,$3,$4)", ctx.guild.id, ctx.author.id, tag_name, tag_text
        )

        await ctx.send(f"``{tag_name}`` was created")

    @tag.command(name="delete")
    async def delete(self, ctx, tag_name):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        if not tag:
            return await ctx.send("No such tag exists.")

        if not await self.can_edit_tag(ctx, tag):
            return await ctx.send("You don't have the permissions to manage this tag.")

        await self.bot.db.fetch(
            "DELETE FROM taggingData "
            "WHERE guild_id = $1 AND tag_name = $2", ctx.guild.id, tag_name
        )

        await ctx.send(f"Deleted tag: ``{tag_name}``")

    @tag.command(name="edit")
    async def edit(self, ctx, tag_name, *, tag_text):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        if not tag:
            return await ctx.send("No such tag exists.")

        if not await self.can_edit_tag(ctx, tag):
            return await ctx.send("You don't have the permissions to manage this tag.")
        
        await self.bot.db.execute(
            "UPDATE taggingData SET tag_text = $1 WHERE guild_id = $2 AND user_added = $3 AND tag_name = $4 ", tag_text,
            ctx.guild.id, ctx.author.id, tag_name)
        await ctx.send(f"Edited tag: ``{tag_name}``")

    @tag.command(name="rename")
    async def rename(self, ctx: commands.Context, tag_name, new_name):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        if not tag:
            return await ctx.send("No such tag exists.")

        new_name_tag = await self.get_tag(ctx.guild.id, new_name)
        if new_name_tag:
            return await ctx.send("There's already a tag with this name")

        if not await self.can_edit_tag(ctx, tag):
            return await ctx.send("You don't have the permissions to manage this tag.")


        await self.bot.db.execute("UPDATE taggingData SET tag_name = $1 WHERE guild_id = $2 AND user_added = $3 ",
                                  new_name, ctx.guild.id, ctx.author.id)
        await ctx.send(f"Renamed ``{tag_name}`` to ``{new_name}``")

    @tag.command(name="search")
    async def search(self, ctx, tag_query):
        cursor = await self.bot.db.fetch("SELECT * FROM taggingData "
            "WHERE guild_id = $1 and tag_name LIKE $2 LIMIT 10",
            ctx.guild.id, tag_query
        )

        if not cursor:
            return await ctx.send("No tags matched that term")

        count = "Maximum of 10" if len(cursor) == 10 else len(cursor)
        lines = "\n".join(rec["tag_name"] for rec in cursor)

        await ctx.send(f"**{count} tags found with search term on this server.**\n```{lines}\n```")


    @tag.command(name="info")
    async def info(self, ctx, *, tag_name):
        tag = await self.get_tag(ctx.guild.id, tag_name)
        
        if not tag:
            return await ctx.send("No such tag exists")

        
        emb = discord.Embed(
            title=f"`{tag_name}`",
        )
        emb.add_field(name="User Added", value=f"<@!{tag['user_added']}>")
        emb.add_field(name="Uses", value=tag["uses"] or 0)

        await ctx.send(embed=emb)
    
    @tag.command(name="list")
    async def list(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        embed = discord.Embed(
            title=f"Tags for {member.name}", 
            description="", 
            color=member.accent_color or 0
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        cursor = await self.bot.db.fetch(
            "SELECT tag_name FROM taggingData "
            "WHERE guild_id = $1 AND user_added = $2", ctx.guild.id, member.id
        )

        if not cursor:
            embed.description = "No tags set"
            return await ctx.send(embed=embed)

        for i, record in enumerate(cursor, start=1):
            embed.description += f"Tag: {i} | Name: {record['tag_name']}\n"

        await ctx.send(embed=embed)
    
    @tag.command(name="all")
    async def all(self, ctx):
        member = ctx.author

        cursor = await self.bot.db.fetch(
            "SELECT tag_name, uses FROM taggingData WHERE guild_id = $1 ORDER BY tag_name", ctx.guild.id
        )

        if not cursor:
            return await ctx.send("No tags found")

        await ctx.send("You'll receive a list of all tags in your DMs shortly.")
        
        try:
            await member.send(f"{len(cursor)} tags found on this server.")
        except discord.Forbidden:
            return await ctx.send("Could not DM you!")
        
        pager = commands.Paginator()

        for record in cursor:
            pager.add_line(line=f"{record['tag_name']} | Uses: {record['uses']}")

        for page in pager.pages:
            await asyncio.sleep(1)
            await ctx.author.send(page)

        await ctx.send("Tags sent in DMs.")


def setup(bot):
    bot.add_cog(TagsCog(bot))
