import pytest
import sys
import os
from pages.login_page import LoginPage
#from pages.register_page import RegisterPage
from pages.my_account_page import AccountPage
from pages.profile_page import ProfilePage
from config.data import Data


# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class BaseTest:
    
    data: Data
    login_page: LoginPage
    my_account_page: AccountPage
    #register_page: RegisterPage
    profile_page: ProfilePage


    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        self.driver = driver
        request.cls.data = Data()
        request.cls.login_page = LoginPage(driver)
        request.cls.my_account_page = AccountPage(driver)
        #request.cls.register_page = RegisterPage(driver)
        request.cls.profile_page = ProfilePage(driver)