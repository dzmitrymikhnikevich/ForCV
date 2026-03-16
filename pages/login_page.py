import allure
import time
import os
from selenium.webdriver.common.by import By
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):

    PAGE_URL = Links.LOGIN_PAGE

    EMAIL_ADDRESS_FIELD = (By.XPATH, "//input[@data-test='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@data-test='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@data-test='login-submit']")
    
    # Запасные локаторы
    EMAIL_FALLBACK_LOCATORS = [
        (By.XPATH, "//input[@type='email']"),
        (By.XPATH, "//input[@name='email']"),
        (By.XPATH, "//input[@id='email']"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name='email']"),
    ]

    @allure.step("Указать почту")
    def enter_email(self, email):
        # Проверяем текущее состояние страницы
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        allure.attach(
            f"URL: {current_url}\nTitle: {page_title}",
            name="Page state before email input",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Делаем скриншот перед вводом
        self.make_screenshot("before_email_input")
        
        # Сохраняем HTML для анализа
        html_content = self.driver.page_source
        allure.attach(
            html_content,
            name="Page HTML",
            attachment_type=allure.attachment_type.HTML
        )
        
        # Ищем все input элементы
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        input_info = "Найденные input элементы:\n"
        for i, inp in enumerate(inputs):
            input_info += f"\n--- Input {i} ---\n"
            input_info += f"type: {inp.get_attribute('type')}\n"
            input_info += f"name: {inp.get_attribute('name')}\n"
            input_info += f"id: {inp.get_attribute('id')}\n"
            input_info += f"class: {inp.get_attribute('class')}\n"
            input_info += f"data-test: {inp.get_attribute('data-test')}\n"
            input_info += f"placeholder: {inp.get_attribute('placeholder')}\n"
            input_info += f"value: {inp.get_attribute('value')}\n"
        
        allure.attach(input_info, name="All input elements", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Пробуем найти поле email
        try:
            # Сначала пробуем основной локатор
            email_field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_ADDRESS_FIELD))
            allure.attach("Найден элемент по data-test='email'", 
                         name="Locator success", 
                         attachment_type=allure.attachment_type.TEXT)
        except TimeoutException:
            allure.attach("Основной локатор не сработал, пробуем запасные", 
                         name="Locator failed", 
                         attachment_type=allure.attachment_type.TEXT)
            
            # Пробуем запасные локаторы
            email_field = None
            for locator in self.EMAIL_FALLBACK_LOCATORS:
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(locator)
                    )
                    allure.attach(f"Найден элемент по локатору: {locator}", 
                                 name="Fallback success", 
                                 attachment_type=allure.attachment_type.TEXT)
                    break
                except:
                    continue
            
            if email_field is None:
                # Если ничего не нашли - сохраняем финальный скриншот
                self.make_screenshot("email_field_not_found")
                raise Exception("Не удалось найти поле email ни по одному локатору")
        
        # Вводим email
        email_field.clear()
        email_field.send_keys(email)
        self.make_screenshot("after_email_input")

    @allure.step("Указать пароль")
    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)

    @allure.step("Кликнуть по кнопке авторизироваться")
    def click_submit_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()    