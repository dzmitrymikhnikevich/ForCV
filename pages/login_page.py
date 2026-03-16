import allure
import time
import os
from selenium.webdriver.common.by import By
from base.base_page import BasePage
from config.links import Links
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


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
    
    # Локаторы для определения Cloudflare страницы
    CLOUDFLARE_INDICATORS = [
        (By.XPATH, "//*[contains(text(), 'Just a moment')]"),
        (By.XPATH, "//*[contains(text(), 'Checking your browser')]"),
        (By.XPATH, "//*[contains(@id, 'cf-content')]"),
        (By.XPATH, "//*[contains(@class, 'cf-browser-verification')]"),
    ]

    def _handle_cloudflare(self):
        """Обработка Cloudflare защиты"""
        print("\n" + "="*50)
        print("🔍 Checking for Cloudflare protection...")
        
        # Проверяем, есть ли признаки Cloudflare
        is_cloudflare = False
        for indicator in self.CLOUDFLARE_INDICATORS:
            try:
                elements = self.driver.find_elements(*indicator)
                if elements and elements[0].is_displayed():
                    is_cloudflare = True
                    print(f"⚠️ Cloudflare detected: {indicator}")
                    break
            except:
                continue
        
        # Дополнительная проверка по заголовку
        if "Just a moment" in self.driver.title or "Checking your browser" in self.driver.title:
            is_cloudflare = True
            print(f"⚠️ Cloudflare detected by title: {self.driver.title}")
        
        if is_cloudflare:
            print("⏳ Waiting for Cloudflare to pass...")
            
            # Делаем скриншот перед ожиданием
            cf_screenshot = f"cloudflare_before_{datetime.now().strftime('%H%M%S')}.png"
            self.driver.save_screenshot(cf_screenshot)
            print(f"📸 Cloudflare screenshot saved: {cf_screenshot}")
            
            # Ждем прохождения Cloudflare (максимум 60 секунд)
            max_wait_time = 60
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                # Проверяем, исчезли ли признаки Cloudflare
                cloudflare_still_present = False
                
                for indicator in self.CLOUDFLARE_INDICATORS:
                    try:
                        elements = self.driver.find_elements(*indicator)
                        if elements and elements[0].is_displayed():
                            cloudflare_still_present = True
                            break
                    except:
                        continue
                
                if not cloudflare_still_present and "Just a moment" not in self.driver.title:
                    print(f"✅ Cloudflare passed after {int(time.time() - start_time)} seconds")
                    
                    # Делаем скриншот после прохождения
                    cf_passed_screenshot = f"cloudflare_after_{datetime.now().strftime('%H%M%S')}.png"
                    self.driver.save_screenshot(cf_passed_screenshot)
                    print(f"📸 Cloudflare passed screenshot: {cf_passed_screenshot}")
                    return True
                
                # Ждем 2 секунды перед следующей проверкой
                time.sleep(2)
            
            # Если Cloudflare не прошел за отведенное время
            print("❌ Cloudflare did not pass within 60 seconds")
            self.driver.save_screenshot("cloudflare_timeout.png")
            
            # Пробуем обновить страницу
            print("🔄 Refreshing page...")
            self.driver.refresh()
            time.sleep(5)
            
            # Проверяем еще раз после обновления
            if "Just a moment" not in self.driver.title:
                print("✅ Cloudflare passed after refresh")
                return True
            
            raise Exception("Cloudflare protection could not be bypassed")
        
        print("✅ No Cloudflare protection detected")
        return False

    @allure.step("Указать почту")
    def enter_email(self, email):
        # Обрабатываем Cloudflare если есть
        self._handle_cloudflare()
        
        # Выводим информацию в консоль
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
    
        # Пробуем найти поле email
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
        print("\n" + "="*50)
        print("🔍 Clicking submit button")
        print(f"URL before click: {self.driver.current_url}")
        
        # Находим и кликаем кнопку
        submit_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        
        # Сохраняем скриншот перед кликом
        self.make_screenshot("before_login_click")
        
        # Кликаем
        submit_button.click()
        print("✓ Submit button clicked")
        
        # Ждем 2 секунды
        time.sleep(2)
        
        # Проверяем URL после клика
        current_url = self.driver.current_url
        print(f"URL after click (2s): {current_url}")
        
        # Сохраняем скриншот после клика
        self.make_screenshot("after_login_click")
        
        # Проверяем, есть ли сообщение об ошибке
        try:
            error_message = self.driver.find_element(By.XPATH, "//*[contains(@class, 'error')]")
            if error_message:
                print(f"❌ Error message found: {error_message.text}")
        except:
            print("✓ No error message found")
        
        # Проверяем, изменился ли URL
        if current_url == Links.LOGIN_PAGE:
            print("⚠️ Still on login page - login might have failed")
            
            # Ищем любые инпуты - возможно, мы все еще на странице логина
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Still have {len(inputs)} inputs on page")
            
            # Сохраняем HTML для анализа
            html_content = self.driver.page_source
            with open("login_page_after_click.html", "w") as f:
                f.write(html_content)
            
            raise Exception("Login failed - still on login page after clicking submit")
        else:
            print(f"✓ URL changed to: {current_url}")