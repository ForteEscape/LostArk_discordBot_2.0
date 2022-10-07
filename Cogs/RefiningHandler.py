from discord import app_commands, Interaction, Object, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View, Select
from Externals.ExceptionHandler import ExceptionHandler
from Externals.RefiningMaterialData import RefiningMaterialData
from Externals.RefiningDataHandler import RefiningDataHandler
from Externals.MaterialCalculator import MaterialCalculator
import random
import discord


class RefiningHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__exception_handler = ExceptionHandler("RefiningHandler").get_logger()
        self.__material_data = RefiningMaterialData()
        self.__update_data = MaterialCalculator()
        self.data_handler = RefiningDataHandler()

    @app_commands.command(name="무기선택")
    async def 무기선택(self, interactions: Interaction):
        uid = str(interactions.user.id)
        is_duplicated = self.data_handler.find_data(uid)

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
                await interaction.response.edit_message(content="강화할 무기가 " + select.values[0] + "무기로 선택되었습니다.")
                data = self.__material_data.get_data(select.values[0])
                cur_step = 0
                if select.values[0] == "유물":
                    cur_step = 15
                elif select.values[0] == "상위유물":
                    cur_step = 11
                elif select.values[0] == "상위고대":
                    cur_step = 11

                success_prob = data.loc[cur_step + 1, "일반성공확률"]
                print(type(success_prob))
                self.data_handler.signup(uid=uid, weapon_class=select.values[0],
                                         cur_step=cur_step, cur_success_probability=success_prob)

            select.callback = select_callback
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            await interactions.response.send_message(view=view)

    @app_commands.command(name="무기삭제")
    async def 무기삭제(self, interactions: Interaction):
        uid = str(interactions.user.id)

        result = self.data_handler.find_data(uid=uid)
        if not result:
            await interactions.response.send_message("무기를 삭제할 수 없습니다. 등록되지 않은 사용자입니다.")
            return

        await interactions.response.send_message("주의!: 무기를 삭제할 경우 해당 무기와 관련된 데이터는 모두 삭제됩니다.")

        try:
            delete_button = Button(style=ButtonStyle.red, label="삭제", disabled=False)
            view = View()
            view.add_item(delete_button)

            async def button_callback(interaction: Interaction):
                self.data_handler.withdraw(uid)
                await interaction.response.edit_message(content="무기가 삭제되었습니다.")

            delete_button.callback = button_callback
        except Exception as e:
            self.__exception_handler.debug(e)
        else:
            await interactions.followup.send(view=view)

    @app_commands.command(name="강화")
    async def 강화(self, interactions: Interaction):
        uid = str(interactions.user.id)
        result = self.data_handler.find_data(uid=uid)

        if not result:
            await interactions.response.send_message("등록되지 않은 유저입니다. 무기선택 명령어를 실행하여 먼저 등록해주세요")
            return

        user_current_step = result[0]['cur_step']
        usr_cur_suc_prob = result[0]['cur_success_prob']
        usr_wpn_cls = result[0]['weapon_class']
        usr_cur_ceiling = result[0]['cur_ceiling_status']

        if user_current_step == 25:
            await interactions.response.send_message("최대 강화치에 도달하였습니다. 강화를 사용하시려면 무기를 초기화해야 합니다.")
            return

        embed = discord.Embed(title=interactions.user.name + " 님 의 무기 강화 정보",
                              description=f"무기 종류: {usr_wpn_cls} 무기\n"
                                          f"현재 무기 강화 단계: {user_current_step} 단계\n"
                                          f"강화 성공 확률: {usr_cur_suc_prob}%\n"
                                          f"장인의 기운: {usr_cur_ceiling}%")
        await interactions.response.send_message(embed=embed)

        if float(usr_cur_ceiling) < 100.0:
            add_refining_helper_selection = Select(placeholder="강화 종류")
            add_refining_helper_selection.add_option(label="숨결 사용", value="풀숨")
            add_refining_helper_selection.add_option(label="숨결 미사용", value="노숨")
        else:
            add_refining_helper_selection = Select(placeholder="강화 종류")
            add_refining_helper_selection.add_option(label="숨결 미사용", value="노숨")

        button = Button(style=ButtonStyle.green, label="button", disabled=False)
        view = View()
        view.add_item(add_refining_helper_selection)
        view.add_item(button)

        material_data = self.__material_data.get_data(usr_wpn_cls)

        async def select_callback(interaction: Interaction):
            add_refining_helper_selection.disabled = True
            await interaction.response.edit_message(content=add_refining_helper_selection.values[0] + " 강화를 선택하셨습니다.")
        add_refining_helper_selection.callback = select_callback

        async def button_callback(interaction: Interaction):
            button.disabled = True
            prob = float(result[0]["cur_success_prob"])
            use_helper = False
            if add_refining_helper_selection.values[0] == "풀숨":
                prob = (prob + material_data.loc[user_current_step + 1, "일반성공확률"]) * 0.01
                use_helper = True
            else:
                prob = prob * 0.01

            rand = random.random()
            datalist = [material_data.loc[user_current_step + 1, "파괴석"],
                        material_data.loc[user_current_step + 1, "돌파석"],
                        material_data.loc[user_current_step + 1, "융화제료"],
                        material_data.loc[user_current_step + 1, "명파"],
                        material_data.loc[user_current_step + 1, "골드"],
                        material_data.loc[user_current_step + 1, "가호"],
                        material_data.loc[user_current_step + 1, "축복"],
                        material_data.loc[user_current_step + 1, "은총"],
                        material_data.loc[user_current_step + 1, "일반성공확률"]
                        ]
            self.__update_data.list_clear()

            try:
                # 강화 성공
                if prob >= rand:
                    self.__update_data.calculate_material(datalist=datalist, is_success=True,
                                                          used_helper=use_helper, db_data_dic=result[0])
                    update_datalist = self.__update_data.get_datalist()
                    self.data_handler.update(datalist=update_datalist, uid=uid)
                    self.data_handler.data_transport(uid=uid)

                    if user_current_step + 1 == 25:
                        new_success_prob = "0.0"
                    else:
                        new_success_prob = str(material_data.loc[user_current_step + 2, "일반성공확률"])
                    self.data_handler.data_init(uid=uid, s_prob=new_success_prob)

                    embed = discord.Embed(title="강화 성공!")
                    embed.add_field(name="개요",
                                    value=f"강화 횟수: {str(update_datalist[0])}회\n"
                                          f"확률: {usr_cur_suc_prob} %\n"
                                          f"장인의 기운: {usr_cur_ceiling} %\n")
                    embed.add_field(name="소모 재료",
                                    value=f"파괴석: {str(update_datalist[1])} 개\n"
                                          f"돌파석: {str(update_datalist[2])} 개\n"
                                          f"융화제: {str(update_datalist[3])} 개\n"
                                          f"명예의 파편: {str(update_datalist[4])} 개\n"
                                          f"골드: {str(update_datalist[5])} 골드\n")
                    embed.add_field(name="소모 숨결",
                                    value=f"가호: {str(update_datalist[6])} 개\n"
                                          f"축복: {str(update_datalist[7])} 개\n"
                                          f"은총: {str(update_datalist[8])} 개\n")

                    await interaction.response.send_message(embed=embed)
                else:
                    self.__update_data.calculate_material(datalist=datalist, is_success=False,
                                                          used_helper=use_helper, db_data_dic=result[0])
                    update_datalist = self.__update_data.get_datalist()
                    self.data_handler.update(datalist=update_datalist, uid=uid)

                    embed = discord.Embed(title="강화 실패...",
                                          description=
                                          f"쌓인 장인의 기운: {str(round(float(update_datalist[-1]) - float(usr_cur_ceiling), 2))}%\n"
                                          f"상승한 성공 확률: {str(float(update_datalist[-2]) - float(usr_cur_suc_prob))}%")

                    await interaction.response.send_message(embed=embed)
            except Exception as e:
                self.__exception_handler.debug(e)
        button.callback = button_callback

        await interactions.followup.send(view=view)

    async def 강화정보(self, interactions: Interaction):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(
        RefiningHandler(bot),
        guilds=[Object(id=827887392047497216), Object(id=863529285553618944)]
    )
