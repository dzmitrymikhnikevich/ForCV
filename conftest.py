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
    
    # === НОВЫЕ НАСТРОЙКИ ДЛЯ ОБХОДА CLOUDFLARE ===
    
    # Отключаем автоматизацию (чтобы сайт не определял, что мы бот)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Устанавливаем реальный User-Agent (как у обычного браузера)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Языковые настройки
    options.add_argument("--lang=en-US,en;q=0.9")
    
    # Включаем поддержку JavaScript
    options.add_argument("--enable-javascript")
    
    # Дополнительные заголовки
    options.add_argument("--accept-lang=en-US")
    options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    
    driver = webdriver.Chrome(options=options)
    
    # === ДОПОЛНИТЕЛЬНЫЙ JAVASCRIPT ДЛЯ СКРЫТИЯ АВТОМАТИЗАЦИИ ===
    
    # Исполняем JavaScript, чтобы скрыть признаки автоматизации
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Добавляем дополнительные свойства, как у реального браузера
    driver.execute_script("""
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        window.chrome = {
            runtime: {}
        };
    """)
    
    # Устанавливаем CDP команды для дополнительной маскировки
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    # Устанавливаем размер окна через CDP
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1920,
        'height': 1080,
        'deviceScaleFactor': 1,
        'mobile': False
    })
    
    request.cls.driver = driver
    yield driver
    driver.quit()