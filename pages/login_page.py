import allure
from selenium.webdriver.common.by import By
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):

    PAGE_URL = Links.LOGIN_PAGE

    EMAIL_ADDRESS_FIELD = ("xpath", "//input[@data-test='email']")
    PASSWORD_FIELD = ("xpath", "//input[@data-test='password']")
    LOGIN_BUTTON = ("xpath", "//input[@data-test='login-submit']")

    @allure.step("Указать почту")
    def enter_email(self, email):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.wait.until(EC.element_to_be_clickable(self.EMAIL_ADDRESS_FIELD)).send_keys(email)

    @allure.step("Указать пароль")
    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)

    @allure.step("Кликнуть по кнопке авторизироваться")
    def click_submit_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()


