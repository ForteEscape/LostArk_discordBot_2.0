from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object
from Externals.DataReader import DataReader


class PlayerContentHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="캐릭터정보")
    async def 캐릭터정보(self, interactions: Interaction, player: str):
        path = './data/user_nickname/user_nickname_list.csv'
        data_reader = DataReader()

        if data_reader.get_data_status():
            data_reader.read_csv(path)

        player_nickname = data_reader.get_data()
        key = player

        for element in player_nickname:
            if player in element:
                key = element[0]
                break

        await interactions.response.send_message(player + "의 정보를 호출합니다\n" + 'https://loawa.com/char/' + key)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        PlayerContentHandler(bot),
        guilds=[Object(id=863529285553618944)]
    )