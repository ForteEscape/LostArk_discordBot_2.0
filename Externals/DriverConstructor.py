from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Externals.ExceptionHandler import ExceptionHandler


class DriverConstructor:
    def __init__(self):
        self.driver_status = False
        self.__exception_handler = ExceptionHandler("DriverConstructor")

    def set_driver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--window-size=1920, 1080")
            # chrome_options.add_argument("--remote-debugging-port=9222")

            # for live service
            # driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

            # ====================== testing service ==================================
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
            # ====================== testing service end ==============================
        except Exception as e:
            self.__exception_handler.print_error(e)
            self.driver_status = False
        else:
            self.driver_status = True

            return driver

    def get_driver_status(self):
        return self.driver_status
