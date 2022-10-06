import re
import discord
from discord.ext import commands
from Externals.ExceptionHandler import ExceptionHandler


class EmojiHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__exception_handler = ExceptionHandler("EmojiHandler").get_logger()

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            m = (re.match(r"^<a?:[\w]+:([\d]+)>$", message.content))

            if m:
                if message.content.startswith("<a:"):
                    ext = "gif"
                else:
                    ext = "png"

                embed = discord.Embed(color=0xffffff)
                if message.author.avatar is None:
                    embed.set_author(name=message.author.display_name)
                else:
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
                embed.set_image(url=f"https://cdn.discordapp.com/emojis/{m.group(1)}.{ext}")

                await message.channel.send(embed=embed)
                await message.delete()
        except Exception as e:
            self.__exception_handler.debug(e)


async def setup(bot):
    await bot.add_cog(EmojiHandler(bot))
