import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN") if os.getenv("DEBUG") == "False" else os.getenv("TEST_TOKEN")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_USER = os.getenv("REDIS_USER")
DATA_FILE = os.getenv("DATA_FILE")
STATIC_FILES = os.getenv("STATIC_FILES")
