from DriverConstructor import DriverConstructor
from selenium.webdriver.common.by import By


class NoticeCrawler(DriverConstructor):
    def __init__(self):
        super().__init__()
        self.previous_notice_maintenance = None
        self.current_notice_maintenance = None
        self.notice_maintenance_article = None
        self.data_crawl_status = False

    def get_maintenance_data(self):
        article_path = '#lostark-wrapper > div > main > div > div.board.board--article > article > section > div'
        title_path = 'a > div.list__subject > span.list__title'
        notice_list_path = '#list > div.list.list--default > ul:nth-child(2) > li'
        notice_path = 'https://lostark.game.onstove.com/News/Notice/List?noticetype=inspection'

        driver = self.get_driver()
        driver.get(notice_path)

        if driver.current_url != notice_list_path:
            driver.quit()
            self.data_crawl_status = False
            return

        if self.previous_notice_maintenance is None and self.current_notice_maintenance is None:
            notice_data = driver.find_elements(By.CSS_SELECTOR, notice_list_path)

            self.previous_notice_maintenance = notice_data[0].find_element(By.CSS_SELECTOR, title_path).text
            self.current_notice_maintenance = notice_data[0].find_element(By.CSS_SELECTOR, title_path).text

            notice_data[0].click()

            notice_article_data = driver.find_element(By.CSS_SELECTOR, article_path)
            self.notice_maintenance_article = notice_article_data.text

            driver.quit()
            self.data_crawl_status = True
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
                return

            driver.quit()
            self.data_crawl_status = False
            return

    def get_crawl_status(self):
        return self.data_crawl_status







