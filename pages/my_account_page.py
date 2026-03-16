import allure
import time
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AccountPage(BasePage):

    PAGE_URL = Links.ACCOUNT_PAGE

    NAV_PROFILE_BUTTON = (By.XPATH, "//a[@data-test='nav-profile']")
    
    # Запасные локаторы на случай, если data-test не работает
    NAV_PROFILE_FALLBACK = [
        (By.XPATH, "//a[contains(@href, 'profile')]"),
        (By.XPATH, "//a[contains(text(), 'Profile')]"),
        (By.XPATH, "//*[@data-test='nav-profile']"),
        (By.XPATH, "//button[@data-test='nav-profile']"),
        (By.XPATH, "//a[@class='nav-link' and contains(text(), 'Profile')]"),
        (By.CSS_SELECTOR, "[data-test='nav-profile']"),
    ]

    @allure.step("Кликнуть по вкладке Профиль")
    def click_nav_profile(self):
        print("\n" + "="*50)
        print("🔍 Clicking profile navigation")
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
        
        # Делаем скриншот перед поиском
        self.make_screenshot("before_profile_click")
        
        # Ждем немного после логина (на всякий случай)
        time.sleep(2)
        
        # Пробуем найти элемент с увеличенным таймаутом
        try:
            # Сначала проверяем наличие элемента в DOM
            self.wait.until(EC.presence_of_element_located(self.NAV_PROFILE_BUTTON))
            print("✓ Profile link found in DOM")
            
            # Затем проверяем, что он кликабельный
            profile_link = self.wait.until(EC.element_to_be_clickable(self.NAV_PROFILE_BUTTON))
            print("✓ Profile link is clickable")
            
        except TimeoutException:
            print("✗ Main locator failed, trying fallbacks...")
            profile_link = None
            
            # Пробуем запасные локаторы
            for locator in self.NAV_PROFILE_FALLBACK:
                try:
                    profile_link = self.wait.until(EC.element_to_be_clickable(locator))
                    print(f"✓ Found by fallback: {locator}")
                    break
                except:
                    print(f"✗ Fallback failed: {locator}")
                    continue
            
            if profile_link is None:
                print("✗ All locators failed!")
                
                # Сохраняем информацию для отладки
                self.make_screenshot("profile_link_not_found")
                
                # Ищем все ссылки на странице
                all_links = self.driver.find_elements(By.TAG_NAME, "a")
                print(f"\nFound {len(all_links)} links on page:")
                for i, link in enumerate(all_links):
                    print(f"\n--- Link {i} ---")
                    print(f"  text: {link.text}")
                    print(f"  href: {link.get_attribute('href')}")
                    print(f"  data-test: {link.get_attribute('data-test')}")
                    print(f"  class: {link.get_attribute('class')}")
                
                # Ищем все элементы с data-test атрибутом
                all_data_test = self.driver.find_elements(By.XPATH, "//*[@data-test]")
                print(f"\nFound {len(all_data_test)} elements with data-test attribute:")
                for elem in all_data_test:
                    print(f"  tag: {elem.tag_name}, data-test: {elem.get_attribute('data-test')}")
                
                raise Exception("Не удалось найти ссылку на профиль ни по одному локатору")
        
        # Прокручиваем к элементу (на всякий случай)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", profile_link)
        time.sleep(0.5)
        
        # Кликаем
        profile_link.click()
        print("✓ Clicked profile link")
        
        # Делаем скриншот после клика
        time.sleep(1)
        self.make_screenshot("after_profile_click")