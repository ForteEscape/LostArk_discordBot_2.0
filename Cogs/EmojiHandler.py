import re
import discord
from discord.ext import commands


class EmojiHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        m = (re.match(r"^<a?:[\w]+:([\d]+)>$", message.content))

        if m:
            if message.content.startswith("<a:"):
                ext = "gif"
            else:
                ext = "png"

            embed = discord.Embed(color=0xffffff)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
            embed.set_image(url=f"https://cdn.discordapp.com/emojis/{m.group(1)}.{ext}")

            await message.channel.send(embed=embed)
            await message.delete()


async def setup(bot):
    await bot.add_cog(EmojiHandler(bot))
