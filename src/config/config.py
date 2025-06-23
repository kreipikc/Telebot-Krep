import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN", "your_telegram_bot_token")