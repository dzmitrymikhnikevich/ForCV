import allure
import time
import os
from selenium.webdriver.common.by import By
from base.base_page import BasePage
from config.links import Links
from datetime import datetime
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
        # Выводим информацию в консоль (это точно увидим в логах GitHub Actions)
        print("\n" + "="*50)
        print("DEBUG: enter_email method called")
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
    
        # Ищем все input элементы и выводим их в консоль
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} input elements:")
        for i, inp in enumerate(inputs):
            print(f"\n--- Input {i} ---")
            print(f"  type: {inp.get_attribute('type')}")
            print(f"  name: {inp.get_attribute('name')}")
            print(f"  id: {inp.get_attribute('id')}")
            print(f"  class: {inp.get_attribute('class')}")
            print(f"  data-test: {inp.get_attribute('data-test')}")
            print(f"  placeholder: {inp.get_attribute('placeholder')}")
        print("="*50)
    
        # Сохраняем скриншот
        screenshot_name = f"debug_email_input_{datetime.now().strftime('%H%M%S')}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"Screenshot saved: {screenshot_name}")
    
        # Пробуем найти поле email (ваш существующий код)
        try:
            email_field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_ADDRESS_FIELD))
            print("✓ Found email field by main locator")
        except TimeoutException:
            print("✗ Main locator failed, trying fallbacks...")
            email_field = None
            for locator in self.EMAIL_FALLBACK_LOCATORS:
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(locator)
                    )
                    print(f"✓ Found by fallback: {locator}")
                    break
                except:
                    print(f"✗ Fallback failed: {locator}")
                    continue
        
            if email_field is None:
                print("✗ All locators failed!")
                self.driver.save_screenshot("email_field_not_found_final.png")
                raise Exception("Не удалось найти поле email ни по одному локатору")
    
        email_field.clear()
        email_field.send_keys(email)
        print("✓ Email entered successfully")

    @allure.step("Указать пароль")
    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)

    @allure.step("Кликнуть по кнопке авторизироваться")
    def click_submit_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()    