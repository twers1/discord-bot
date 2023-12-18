import os
from dotenv import load_dotenv

# Библиотека для загрузки данных из файла ENV
load_dotenv()

# Подключение переменных из файла ENV
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
