import allure
import os
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        # Увеличиваем таймаут для CI/CD окружения
        timeout = 30 if os.getenv('CI') else 10  # 30 сек для GitHub, 10 для локалки
        self.wait = WebDriverWait(driver, timeout, poll_frequency=1)


    def open(self):
        if not hasattr(self, 'PAGE_URL') or self.PAGE_URL is None:
            raise AttributeError("PAGE_URL must be defined in child class")
    
        with allure.step(f"Open {self.PAGE_URL} page"):
            self.driver.get(self.PAGE_URL)
            # Ждем загрузки страницы
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def is_opened(self):
        if not hasattr(self, 'PAGE_URL') or self.PAGE_URL is None:
            raise AttributeError("PAGE_URL must be defined in child class")
    
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            self.wait.until(EC.url_to_be(self.PAGE_URL))

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )