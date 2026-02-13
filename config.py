from decouple import config
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

API_ID = config("API_ID", cast=int)
API_HASH = config("API_HASH", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=str)