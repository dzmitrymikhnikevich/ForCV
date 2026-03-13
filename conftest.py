import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(scope="function", autouse=True)
def driver(request):
    options = Options()
    # Базовые настройки для Docker
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
     # Дополнительные настройки для стабильности
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9222")
    # Игнорируем ошибки сертификатов
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    yield driver
    driver.quit()