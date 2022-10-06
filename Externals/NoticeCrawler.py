from Externals.DriverConstructor import DriverConstructor
from selenium.webdriver.common.by import By
from Externals.DataReader import DataReader
from Externals.ExceptionHandler import ExceptionHandler
from Externals.DataWriter import DataWriter


class NoticeCrawler(DriverConstructor):
    def __init__(self):
        super().__init__()

        self.previous_notice_maintenance = None
        self.current_notice_maintenance = None
        self.notice_maintenance_article = None
        self.data_crawl_status = None
        self.data_reader = DataReader()
        self.data_writer = DataWriter()
        self.__exception_handler = ExceptionHandler("NoticeCrawler").get_logger()

    def get_maintenance_data(self):
        article_path = '#lostark-wrapper > div > main > div > div.board.board--article > article > section > div'
        title_path = 'a > div.list__subject > span.list__title'
        notice_list_path = '#list > div.list.list--default > ul:nth-child(2) > li'
        notice_path = 'https://lostark.game.onstove.com/News/Notice/List?noticetype=inspection'

        driver = self.set_driver()
        driver.get(notice_path)

        if not self.driver_status:
            return

        if driver.current_url != notice_path:
            driver.quit()
            self.data_crawl_status = False
            return

        try:
            if self.previous_notice_maintenance is None and self.current_notice_maintenance is None:
                path = './data/notice_data/notice.txt'
                self.data_reader.read_txt(path)
                temp_data = self.data_reader.get_raw_data()
                notice_data = driver.find_elements(By.CSS_SELECTOR, notice_list_path)

                self.previous_notice_maintenance = notice_data[0].find_element(By.CSS_SELECTOR, title_path).text
                self.current_notice_maintenance = notice_data[0].find_element(By.CSS_SELECTOR, title_path).text

                notice_data[0].click()

                notice_article_data = driver.find_element(By.CSS_SELECTOR, article_path)
                self.notice_maintenance_article = notice_article_data.text

                if temp_data == self.notice_maintenance_article:
                    driver.quit()
                    self.data_crawl_status = False
                    return

                driver.quit()
                self.data_crawl_status = True
                self.__store_notice(self.notice_maintenance_article)
                return
            else:
                notice_data = driver.find_elements(By.CSS_SELECTOR, notice_list_path)
                self.current_notice_maintenance = notice_data[0].find_element(By.CSS_SELECTOR, title_path).text

                # 만약 제목이 같지 않다 -> 공지 리스트에 변경이 생겼다
                if self.current_notice_maintenance != self.previous_notice_maintenance:
                    notice_data[0].click()
                    notice_article_data = driver.find_element(By.CSS_SELECTOR, article_path)
                    self.notice_maintenance_article = notice_article_data.text
                    self.previous_notice_maintenance = self.current_notice_maintenance

                    driver.quit()

                    self.data_crawl_status = True
                    self.__store_notice(notice_article_data.text)
                    return

                driver.quit()
                self.data_crawl_status = False
                return
        except Exception as e:
            self.__exception_handler.debug(e)

    def get_crawl_status(self):
        return self.data_crawl_status

    def __store_notice(self, notice_data):
        self.data_writer.write_text("./data/notice_data/notice.txt", notice_data)







