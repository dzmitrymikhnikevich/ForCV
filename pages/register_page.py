from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC


class registerPage(BasePage):

    PAGE_URL = Links.REGISTER_PAGE

    FIRST_NAME_FIELD = ("xpath", "//input[@data-test='first-name']")
    LAST_NAME_FIELD = ("xpath", "//input[@data-test='last-name']")
    DATE_OF_BIRTH_FIELD = ("xpath", "//input[@data-test='dob']")
    STREET_FIELD = ("xpath", "//input[@data-test='street']")
    POSTAL_CODE_FIELD = ("xpath", "//input[@data-test='postal-code']")
    CITY_FIELD = ("xpath", "//input[@data-test='city']")
    STATE_FIELD = ("xpath", "//input[@data-test='state']")
    COUNTRY_FIELD = ("xpath", "//input[@data-test='country']")
    PHONE_FIELD = ("xpath", "//input[@data-test='phone']")
    EMAIL_FIELD = ("xpath", "//input[@data-test='email']")
    PASSWORD_FIELD = ("xpath", "//input[@data-test='password']")
    REGISTER_BUTTON = ("xpath", "//input[@data-test='register-submit']")


    def enter_first_name(self, first_name):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD)).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_FIELD)).send_keys(last_name)

    def enter_date_of_birth(self, date_of_birth):
        self.wait.until(EC.element_to_be_clickable(self.DATE_OF_BIRTH_FIELD)).send_keys(date_of_birth)

    def enter_street(self, street):
        self.wait.until(EC.element_to_be_clickable(self.STREET_FIELD)).send_keys(street)

    def enter_postal_code(self, postal_code):
        self.wait.until(EC.element_to_be_clickable(self.POSTAL_CODE_FIELD)).send_keys(postal_code)

    def enter_city(self, city):
        self.wait.until(EC.element_to_be_clickable(self.CITY_FIELD)).send_keys(city)

    def enter_state(self, state):
        self.wait.until(EC.element_to_be_clickable(self.STATE_FIELD)).send_keys(state)

    def enter_country(self, country):
        self.wait.until(EC.element_to_be_clickable(self.COUNTRY_FIELD)).send_keys(country)

    def enter_phone(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_FIELD)).send_keys(phone)

    def enter_email_address(self, email_address):
        self.wait.until(EC.element_to_be_clickable(self.EMAIL_FIELD)).send_keys(email_address)

    def enter_password(self, password):
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)

    def click_register_button(self):
        self.wait.until(EC.element_to_be_clickable(self.REGISTER_BUTTON)).click()

    
