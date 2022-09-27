from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverConstructor:
    def __init__(self):
        self.__driver = self.__set_driver()

    def __set_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--window-size=1920, 1080")
        # chrome_options.add_argument("--remote-debugging-port=9222")

        # for live service
        driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

        # ====================== testing service ==================================
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
        # ====================== testing service end ==============================

        return driver

    def get_driver(self):
        return self.__driver
