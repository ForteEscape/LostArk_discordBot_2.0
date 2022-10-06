import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object
from Externals.DataReader import DataReader
from Externals.ExceptionHandler import ExceptionHandler


class PlayerContentHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data_reader = DataReader()
        self.__exception_handler = ExceptionHandler("PlayerContentHandler").get_logger()

    @app_commands.command(name="캐릭터정보")
    async def 캐릭터정보(self, interactions: Interaction, player: str):
        try:
            path = './data/user_nickname/user_nickname_list.csv'

            self.data_reader.read_csv(path)

            player_nickname = self.data_reader.get_data()
            key = player

            for element in player_nickname:
                if player in element:
                    key = element[0]
                    break

            await interactions.response.send_message(player + "의 정보를 호출합니다\n" + 'https://loawa.com/char/' + key)
        except Exception as e:
            self.__exception_handler.debug(e)

    @app_commands.command(name="각인")
    async def 각인(self, interactions: Interaction, engrave_name: str):
        try:
            nickname_path = './data/engrave_data/engrave_nickname.csv'
            description_path = './data/engrave_data/engrave_description.csv'

            self.data_reader.read_csv(nickname_path)

            engrave_name_data = self.data_reader.get_data()
            key = engrave_name

            for element in engrave_name_data:
                if key in element:
                    key = element[0]
                    break

            self.data_reader.read_csv(description_path)
            engrave_description_data = self.data_reader.get_data()
            engrave_description = ""

            for engrave in engrave_description_data:
                if key == engrave[0]:
                    engrave_description = engrave[1]

            if engrave_description != "":
                embed = discord.Embed(title=key + " 각인 설명",
                                      description=engrave_description)
                await interactions.response.send_message(embed=embed)
            else:
                await interactions.response.send_message(key + " 각인은 존재하지 않는 각인이거나 추가되지 않은 각인입니다.")
        except Exception as e:
            self.__exception_handler.debug(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        PlayerContentHandler(bot),
        guilds=[Object(id=827887392047497216), Object(id=863529285553618944)]
    )
