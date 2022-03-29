import discord 
from discord.ext import commands
import os
import asyncpg
from dotenv import load_dotenv



load_dotenv()

os.environ.setdefault("JISHAKU_HIDE", "1")
os.environ.setdefault("JISHAKU_RETAIN", "1")
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")

description ="I Am an  Ai Chat Bot "
intents = discord.Intents.default()
intents.members = True


bot= commands.Bot(command_prefix="?", description=description, intents=intents)

for name in os.listdir("./cogs"):
    if name.endswith(".py"):
        cog_name = f"cogs.{os.path.splitext(name)[0]}"

        try:
            bot.load_extension(cog_name)
        except Exception as e:
            print(f"Error in loading {cog_name}: {e.__class__.__name__}: {e}")


@bot.event
async def on_ready():
    bot.db = await asyncpg.create_pool(database=os.getenv("POSTGRES_DB_NAME"),
                                        port=os.getenv("POSTGRES_PORT"),
                                        host="containers-us-west-28.railway.app",
                                        password=os.getenv("POSTGRES_PASS"),
                                        user=os.getenv("POSTGRES_USER"),
                                        max_inactive_connection_lifetime=3)
    if not bot.db:
        raise NotImplementedError("Postgres DB is not online")

    await bot.db.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    await bot.db.execute(
        "CREATE TABLE IF NOT EXISTS taggingData "
        "(guild_id BIGINT, user_added BIGINT, uses INTEGER, tag_name TEXT, tag_text TEXT)"
    )
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    



bot.run(os.getenv("TOKEN"))
