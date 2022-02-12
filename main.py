import discord 
from discord.ext import commands
import os

from dotenv import load_dotenv



load_dotenv()

os.environ.setdefault("JISHAKU_HIDE", "1")
os.environ.setdefault("JISHAKU_RETAIN", "1")
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")

description ="I Am an  Ai Chat Bot "
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="w!", description=description, intents=intents)

# -- load all cogs
for name in os.listdir("./cogs"):
    if name.endswith(".py"):
        cog_name = f"cogs.{os.path.splitext(name)[0]}"

        try:
            bot.load_extension(cog_name)
        except Exception as e:
            print(f"Error in loading {cog_name}: {e.__class__.__name__}: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")



bot.run(os.getenv("TOKEN"))