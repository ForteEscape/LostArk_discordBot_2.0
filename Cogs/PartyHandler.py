from discord.ext import commands, tasks
from discord import Object
from Externals.PartyDataReader import PartyDataReader
from Externals.PartyDataWriter import PartyDataWriter
from Externals.PartyData import PartyData
from Externals.ExceptionHandler import ExceptionHandler
from pytz import timezone
import datetime
import requests
import os
import glob


class PartyHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data_reader = PartyDataReader()
        self.data_writer = PartyDataWriter()
        self.party_data = PartyData()
        self.__exception_handler = ExceptionHandler("PartyHandler")
        self.party_data.make_output_data()
        self.party_alarm.start()

    @tasks.loop(seconds=1)
    async def party_alarm(self):
        try:
            total_party_data = self.party_data.get_output_list()
            if not total_party_data:
                return

            days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            chk_time = datetime.datetime.now(timezone('Asia/Seoul')) + datetime.timedelta(seconds=1800)
            day_of_week = days[chk_time.weekday()]

            announce_party = []

            abrel_party_list = [
                "노브1~6", "하브1~6", "노브1~4", "하브1~4",
                "노브1~2", "노브3~4", "노브5~6", "하브1~2",
                "하브3~4", "하브5~6", "하브1~2노브3~4", "하브1~2노브3~6",
                "하브1~4노브5~6"
            ]

            illiakan_party_list = ["아칸노말", "아칸하드", "에피데믹"]

            for element in total_party_data:
                if element[2] == day_of_week:
                    announce_party.append(element)

            party_member_id = self.data_reader.get_member_id()
            if not party_member_id:
                self.data_reader.read_csv("./data/party_data/member_id.csv")
                party_member_id = self.data_reader.get_member_id()

            for data in announce_party:
                party_time = data[3].split()

                for index in range(len(data[4])):
                    for element in party_member_id:
                        if data[4][index] in element:
                            data[4][index] = element[1]

                party_data = data[0].split()[1]

                if len(party_time) == 1:
                    if chk_time.hour == int(party_time[0]) and chk_time.minute == 0 and chk_time.second == 0:
                        if party_data in abrel_party_list:
                            # 아브렐슈드 채널
                            # channel = self.bot.get_channel(998535769977262170)
                            channel = self.bot.get_channel(1024960497122029609)
                            await channel.send(data[0] + " 파티에 대한 인원 입니다.")
                            await channel.send(f"```\n{data[1]}\n```")
                            await channel.send(f"<@{data[4][0]}> <@{data[4][1]}> <@{data[4][2]}> <@{data[4][3]}> "
                                               f"<@{data[4][4]}> <@{data[4][5]}> <@{data[4][6]}> <@{data[4][7]}>")
                        elif party_data in illiakan_party_list:
                            # channel = self.bot.get_channel(1006737870268158003)
                            channel = self.bot.get_channel(1024960481221423134)
                            await channel.send(data[0] + " 파티에 대한 인원 입니다.")
                            await channel.send(f"```\n{data[1]}\n```")
                            await channel.send(f"<@{data[4][0]}> <@{data[4][1]}> <@{data[4][2]}> <@{data[4][3]}> "
                                               f"<@{data[4][4]}> <@{data[4][5]}> <@{data[4][6]}> <@{data[4][7]}>")
                else:
                    if chk_time.hour == int(party_time[0]) and chk_time.minute == int(
                            party_time[1]) and chk_time.second == 0:
                        if party_data in abrel_party_list:
                            # 아브렐슈드 채널
                            # channel = self.bot.get_channel(998535769977262170)
                            channel = self.bot.get_channel(1024960497122029609)
                            await channel.send(data[0] + " 파티에 대한 인원 입니다.")
                            await channel.send(f"```\n{data[1]}\n```")
                            await channel.send(f"<@{data[4][0]}> <@{data[4][1]}> <@{data[4][2]}> <@{data[4][3]}> "
                                               f"<@{data[4][4]}> <@{data[4][5]}> <@{data[4][6]}> <@{data[4][7]}>")
                        elif party_data in illiakan_party_list:
                            # channel = self.bot.get_channel(1006737870268158003)
                            channel = self.bot.get_channel(1024960481221423134)
                            await channel.send(data[0] + " 파티에 대한 인원 입니다.")
                            await channel.send(f"```\n{data[1]}\n```")
                            await channel.send(f"<@{data[4][0]}> <@{data[4][1]}> <@{data[4][2]}> <@{data[4][3]}> "
                                               f"<@{data[4][4]}> <@{data[4][5]}> <@{data[4][6]}> <@{data[4][7]}>")
        except Exception as e:
            self.__exception_handler.print_error(e)
    @commands.command()
    async def 파티설정(self, ctx):
        try:
            path_reading = './data/party_data/party_data.txt'
            path_write_prefix = './data/party_data/'
            path_party_list = './data/party_data/party_list.txt'
            [os.remove(f) for f in glob.glob("./data/party_data/*.txt")]
            self.party_data.clear_data()

            attachment_url = ctx.message.attachments[0].url
            file_request = requests.get(attachment_url)
            file_request.encoding = 'UTF-8'

            with open(path_reading, 'w', newline='') as party_file:
                party_file.write(file_request.text)

            self.data_reader.read_txt(path_reading)
            party_data_raw = self.data_reader.get_raw_party_data()

            self.data_writer.write_party_text(path_write_prefix, party_data_raw)
            self.data_writer.write_text(path_party_list, self.data_writer.get_party_name_list())

            self.party_data.make_output_data()

            participate_weekly_member_list = []
            party_output_data = self.party_data.get_output_list()

            for element in party_output_data:
                participate_member = element[4]

                for member in participate_member:
                    if (member not in participate_weekly_member_list) and (
                            member not in ["공석", "서폿", "워로드", "홀나", "지인"]):
                        participate_weekly_member_list.append(member)

            if len(participate_weekly_member_list) <= 4:
                await ctx.send("참여자가 너무 작아 수동으로 호출해주셔야 합니다.")
            else:
                self.data_reader.read_csv("./data/party_data/member_id.csv")
                member_id = participate_weekly_member_list
                total_member_id = self.data_reader.get_member_id()
                for index in range(len(member_id)):
                    for element in total_member_id:
                        if member_id[index] in element:
                            member_id[index] = element[1]

                abrel_party_list = [
                    "노브1~6", "하브1~6", "노브1~4", "하브1~4",
                    "노브1~2", "노브3~4", "노브5~6", "하브1~2",
                    "하브3~4", "하브5~6", "하브1~2노브3~4", "하브1~2노브3~6",
                    "하브1~4노브5~6"
                ]

                illiakan_party_list = ["아칸노말", "아칸하드", "에피데믹"]
                for element in party_output_data:
                    party = element[0].split()[1]
                    if party in abrel_party_list:
                        # channel = self.bot.get_channel(998535769977262170)
                        channel = self.bot.get_channel(1024960497122029609)
                        await channel.send(element[0] + " 파티에 대한 인원 입니다.")
                        await channel.send(f"```\n{element[1]}\n```")
                    elif party in illiakan_party_list:
                        # channel = self.bot.get_channel(1006737870268158003)
                        channel = self.bot.get_channel(1024960481221423134)
                        await channel.send(element[0] + " 파티에 대한 인원 입니다.")
                        await channel.send(f"```\n{element[1]}\n```")

                if len(member_id) == 5:
                    await ctx.send(f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> "
                                                             f"<@{member_id[3]}> <@{member_id[4]}>")
                elif len(member_id) == 6:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}>")
                elif len(member_id) == 7:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}>")
                elif len(member_id) == 8:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}>")
                elif len(member_id) == 9:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}>")
                elif len(member_id) == 10:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}>")
                elif len(member_id) == 11:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}> "
                        f"<@{member_id[10]}>")
                elif len(member_id) == 12:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}> "
                        f"<@{member_id[10]}> <@{member_id[11]}>")
                elif len(member_id) == 13:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}> "
                        f"<@{member_id[10]}> <@{member_id[11]}> <@{member_id[12]}>")
                elif len(member_id) == 14:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}> "
                        f"<@{member_id[10]}> <@{member_id[11]}> <@{member_id[12]}> <@{member_id[13]}>")
                elif len(member_id) == 15:
                    await ctx.send(
                        f"<@{member_id[0]}> <@{member_id[1]}> <@{member_id[2]}> <@{member_id[3]}> <@{member_id[4]}> "
                        f"<@{member_id[5]}> <@{member_id[6]}> <@{member_id[7]}> <@{member_id[8]}> <@{member_id[9]}> "
                        f"<@{member_id[10]}> <@{member_id[11]}> <@{member_id[12]}> <@{member_id[13]}> <@{member_id[14]}>")
        except Exception as e:
            self.__exception_handler.print_error(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        PartyHandler(bot),
        guilds=[Object(id=827887392047497216), Object(id=863529285553618944)]
    )