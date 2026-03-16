import allure
import time
from base.base_page import BasePage
from config.links import Links
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class ProfilePage(BasePage):

    PAGE_URL = Links.PROFILE_PAGE

    FIRST_NAME_FIELD = (By.XPATH, "//input[@data-test='first-name']")
    UPDATE_PROFILE_BUTTON = (By.XPATH, "//button[@data-test='update-profile-submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@role='alert' and contains(@class, 'alert-success')]")


    def get_first_name_value(self):
        "Получает текущее значение поля First Name"
        field = self.wait.until(EC.presence_of_element_located(self.FIRST_NAME_FIELD))
        return field.get_attribute("value")


    def change_first_name(self, new_name):
            with allure.step(f"Изменяем значение поля 'First name' на '{new_name}'"):
                first_name_field = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
                first_name_field.click()
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].value = '';", first_name_field)
                first_name_field.send_keys(new_name)
                first_name_field.send_keys(Keys.TAB)
                self.wait.until(
                lambda driver: first_name_field.get_attribute("value") == new_name, f"Значение не стало '{new_name}'"
                )
                assert first_name_field.get_attribute("value") == new_name, "Ошибка ввода"
                self.current_name = new_name


    @allure.step("Кликаем по кнопке 'Update profile'")
    def click_update_profile_button(self):
        self.wait.until(EC.element_to_be_clickable(self.UPDATE_PROFILE_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
        self.wait.until(
        lambda driver: self.get_first_name_value() == self.current_name,
        "Данные не сохранились"
        )


    @allure.step("Проверяем, что изменения сохранены")
    def is_changes_saved(self, expected_name):
        self.driver.refresh()
        first_name_field = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_FIELD))
        self.wait.until(
        lambda driver: self.get_first_name_value() != "",
        "Поле осталось пустым после загрузки"
        )
        current_value = first_name_field.get_attribute("value")

        print(f"\n=== ДИАГНОСТИКА ===")
        print(f"Ожидаемое значение: '{expected_name}'")
        print(f"Фактическое значение: '{current_value}'")
        print(f"Длина ожидаемого: {len(expected_name)}")
        print(f"Длина фактического: {len(current_value)}")

        assert current_value == expected_name