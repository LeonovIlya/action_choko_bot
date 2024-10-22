import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOG_FILE = os.getenv('LOG_FILE')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
ADMIN_ID = os.getenv('ADMIN_ID')
RATE_LIMIT = os.getenv('RATE_LIMIT')
