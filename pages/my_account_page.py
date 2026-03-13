import allure
from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC


class AccountPage(BasePage):

    PAGE_URL = Links.ACCOUNT_PAGE

    NAV_PROFILE_BUTTON = ("xpath", "//a[@data-test='nav-profile']")

    @allure.step("Кликнуть по вкладке Профиль")
    def click_nav_profile(self):
        self.wait.until(EC.presence_of_element_located(self.NAV_PROFILE_BUTTON))
        self.wait.until(EC.element_to_be_clickable(self.NAV_PROFILE_BUTTON)).click()
