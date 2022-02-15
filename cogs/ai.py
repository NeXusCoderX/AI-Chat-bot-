from re import I
from async_timeout import timeout
import discord
from discord.ext import commands
import asyncio

from dotenv import load_dotenv
import os
import requests
load_dotenv()


class AIChatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    @commands.Cog.listener()
    async def on_message(self,message):
        if self.bot.user == message.author:
            return
        if message.channel.id in (
            939722233763479604,940261893833125948,942930685927260201,942930720861618247
            
        ):
            url = (os.getenv("url"))

            querystring = {"server":"main",
            "msg":message.content,
            "bot_name":"Connexa Ai",
            "bot_gender":"male",
            "bot_master":"The_Crush_Kid#0161",
            "bot_age":"39",
            "bot_company":"Weird Medicology",
            "bot_location":"USA",
            "bot_email":"cantprovideemail@gmail.com",
            "bot_build":"Private",
            "bot_birth_year":"2000",
            "bot_birth_date":"1st January, 2000",
            "bot_birth_place":" Discord Weird Medicology Comunity",
            "bot_favorite_color":"Blue",
            "bot_favorite_book":"Harry Potter",
            "bot_favorite_band":"Imagine Doggos",
            "bot_favorite_artist":"PHYSICIANFT#7581",
            "bot_favorite_actress":"Emma Watson ",
            "bot_favorite_actor":"Jim Carrey ",
            "id":"For customised response for each user"}

            headers = {
                'authorization': (os.getenv("auth")),
                'x-rapidapi-host': (os.getenv("host")),
                'x-rapidapi-key': (os.getenv("key"))
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            res = response.json()
        if not message.channel.id in (939722233763479604,940261893833125948,942930685927260201):
            return
        elif message.content.startswith("Connexa when is the drop"):
            await message.channel.trigger_typing()
            typingcat = await message.reply("https://tenor.com/view/cat-computer-typing-fast-gif-5368357")
            await asyncio.sleep(1.5)
            await typingcat.edit("Genesis Epoch is 2/19")

        elif message.content.startswith("Connexa how much?"):
            await message.channel.trigger_typing()
            typingcat = await message.reply("https://tenor.com/view/cat-computer-typing-fast-gif-5368357")
            await asyncio.sleep(1.5)
            await typingcat.edit(" 35 matic presale, 45 public sale")

        elif message.content.startswith('Connexa'):
            await message.channel.trigger_typing()
            typingcat = await message.reply("https://tenor.com/view/cat-computer-typing-fast-gif-5368357")
            await asyncio.sleep(1.5)
            await typingcat.edit(res["AIResponse"],
                    allowed_mentions=discord.AllowedMentions(
                        users=False, roles=False, everyone=False
                    ))


def setup(bot):
    bot.add_cog(AIChatbot(bot))
