import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object
from Externals.BidCalculator import BidCalculator


class MarketHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="경매")
    async def 경매(self, interactions: Interaction, price: int):
        bid_calculator = BidCalculator()

        bid_calculator.calculate(price)
        bid_datalist = bid_calculator.get_bid_data()

        embed = discord.Embed(title="경매가 계산 결과")

        embed.add_field(name=str(price) + "골드 에 대한 4인 경매 입찰 추천 가격",
                        value="4인 입찰 추천 경매가는 " + str(bid_datalist[3]) + "골드\n 4인 분배 입찰 골드는 " +
                              str(bid_datalist[2]) + "골드 입니다.\n")

        embed.add_field(name=str(price) + "골드 에 대한 8인 경매 입찰 추천 가격",
                        value="8인 입찰 추천 경매가는 " + str(bid_datalist[1]) + "골드\n 8인 분배 입찰 골드는 "
                              + str(bid_datalist[0]) + "골드 입니다.\n")

        await interactions.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        MarketHandler(bot),
        guilds=[Object(id=863529285553618944)]
    )