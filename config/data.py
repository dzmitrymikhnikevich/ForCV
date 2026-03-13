import os
from dotenv import load_dotenv

load_dotenv()

class Data:

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")


    # Проверка, что переменные загружены
    def __init__(self):
        if not self.EMAIL or not self.PASSWORD:
            raise ValueError("EMAIL и PASSWORD должны быть установлены в .env файле")