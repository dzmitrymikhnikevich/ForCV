import random
import allure
import pytest
import sys
import os
from base.base_test import BaseTest


# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@allure.feature("Функциональность во вкладке Profile")
class TestProfileFeature(BaseTest):

    @allure.title("Изменение значения 'First name'")
    @allure.severity("Critical")
    @pytest.mark.smoke
    def test_change_profile_first_name(self):
        self.login_page.open()
        self.login_page.enter_email(self.data.EMAIL)
        self.login_page.enter_password(self.data.PASSWORD)
        self.login_page.click_submit_button()
        #self.my_account_page.is_opened()
        self.my_account_page.click_nav_profile()
        new_name = f"Test {random.randint(1, 100)}"
        self.profile_page.change_first_name(new_name)
        self.profile_page.click_update_profile_button()
        self.profile_page.is_changes_saved(new_name)