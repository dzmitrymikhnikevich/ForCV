import allure
import os
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        # Увеличиваем таймаут для CI/CD окружения
        timeout = 30 if os.getenv('CI') else 10  # 30 сек для GitHub, 10 для локалки
        self.wait = WebDriverWait(driver, 10, poll_frequency=1)


    def open(self):
        with allure.step(f"Open {self.PAGE_URL} page"):
            self.driver.get(self.PAGE_URL)

# Метод проверяет, что та страница, которую открывали, открылась
    def is_opened(self):
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            self.wait.until(EC.url_to_be(self.PAGE_URL))


    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )