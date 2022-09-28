from Externals.NoticeCrawler import NoticeCrawler
from pytz import timezone
import discord
import datetime
from discord import Object
from discord.ext import commands, tasks
from Externals.ExceptionHandler import ExceptionHandler


class MaintenanceHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.notice_crawler = NoticeCrawler()
        self.notice_update.start()
        self.__exception_handler = ExceptionHandler("MaintenanceHandler")

    """
    # 매일 매시 02, 32분에 공지 데이터를 읽어와 차이가 있을 경우에 최신 공지를 출력한다.
    # 서버를 다시 재기동 하였을 때 이미 공지한 내용을 다시 공지하는 것을 회피하기 위해 읽어온 공지를 텍스트 파일로
    # 저장하는 방법으로 해야한다고 생각됨
    # 해당 방식으로 구현 완료
    """

    @tasks.loop(seconds=1)
    async def notice_update(self):
        chk_time = datetime.datetime.now(timezone('Asia/Seoul'))

        if (chk_time.minute == 2 and chk_time.now().second == 0) or (chk_time.minute == 32 and chk_time.second == 0):
            try:
                is_change = self.notice_crawler.get_crawl_status()

                if is_change is None:
                    self.notice_crawler.get_maintenance_data()
                    is_not_duplicated = self.notice_crawler.get_crawl_status()

                    if is_not_duplicated:
                        channel = self.bot.get_channel(863529285553618947)

                        embed = discord.Embed(title=self.notice_crawler.previous_notice_maintenance)
                        embed.add_field(name="내용", value=self.notice_crawler.notice_maintenance_article)

                        await channel.send(embed=embed)

                elif is_change:
                    # live service
                    # channel = self.bot.get_channel(945592198165069834)
                    channel = self.bot.get_channel(863529285553618947)

                    embed = discord.Embed(title=self.notice_crawler.previous_notice_maintenance)
                    embed.add_field(name="내용", value=self.notice_crawler.notice_maintenance_article)

                    await channel.send(embed=embed)
            except Exception as e:
                self.__exception_handler.print_error(e)
                return


async def setup(bot: commands.Bot):
    await bot.add_cog(
        MaintenanceHandler(bot),
        guilds=[Object(id=863529285553618944)]
    )
