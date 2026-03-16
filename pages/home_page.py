from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):

    PAGE_URL = Links.HOST

    NAV_MENU_BUTTON = (By.XPATH, //input[@data-test='nav-menu'])
    NAV_MY_ACCOUNT_BUTTON = (By.XPATH, //input[@data-test='nav-my-account'])


    def click_nav_menu_link(self):
        self.wait.until(EC.element_to_be_clickable(self.NAV_MENU_BUTTON)).click()
    
    def click_nav_my_account(self):
        self.wait.until(EC.element_to_be_clickable(self.NAV_MY_ACCOUNT_BUTTON)).click()
