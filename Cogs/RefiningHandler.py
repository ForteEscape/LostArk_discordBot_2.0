from discord import app_commands, Interaction, Object, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View, Select
from Externals.ExceptionHandler import ExceptionHandler
from Externals.DataReader import DataReader
from Externals.RefiningDataHandler import RefiningDataHandler


class RefiningHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__exception_handler = ExceptionHandler("RefiningHandler").get_logger()
        self.data_reader = DataReader()
        self.data_handler = RefiningDataHandler()

    @app_commands.command(name="무기선택")
    async def 무기선택(self, interactions: Interaction):
        uid = str(interactions.user.id)
        is_duplicated = self.data_handler.ready_signup(uid)

        if is_duplicated:
            await interactions.response.send_message("이미 등록한 무기가 존재합니다. 재등록을 원할 시 무기 삭제 명령어를 사용하세요")
            return

        try:
            select = Select(placeholder="무기종류")
            select.add_option(label="유물(1340~1575)", value='유물')
            select.add_option(label="상위유물~고대(1490~1615)", value="상위유물")
            select.add_option(label="상위고대(1580~1650)", value="상위고대")
            view = View()
            view.add_item(select)

            async def select_callback(interaction: Interaction):
                await interaction.response.send_message("강화할 무기가 " + select.values[0] + "무기로 선택되었습니다.")
                self.data_handler.signup(uid, select.values[0])

            select.callback = select_callback
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            await interactions.response.send_message(view=view)

    @app_commands.command(name="무기삭제")
    async def 무기삭제(self, interactions: Interaction):
        uid = str(interactions.user.id)
        await interactions.response.send_message("주의!: 무기를 삭제할 경우 해당 무기와 관련된 데이터는 모두 삭제됩니다.")

        try:
            delete_button = Button(style=ButtonStyle.red, label="삭제", disabled=False)
            view = View()
            view.add_item(delete_button)

            async def button_callback(interactions: Interaction):
                self.data_handler.withdraw(uid)
                await interactions.response.send_message("무기가 삭제되었습니다.")

            delete_button.callback = button_callback
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            await interactions.followup.send(view=view)

    @app_commands.command(name="강화")
    async def 강화(self, interactions: Interaction):
        button = Button(style=ButtonStyle.green, label="button", disabled=False)
        view = View()
        view.add_item(button)

        async def button_callback(interactions: Interaction):
            await interactions.response.edit_message(content="pushed")
        button.callback = button_callback

        await interactions.response.send_message(view=view)

    async def 강화정보(self, interactions: Interaction):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(
        RefiningHandler(bot),
        guilds=[Object(id=827887392047497216), Object(id=863529285553618944)]
    )
