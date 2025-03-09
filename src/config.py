import os
import logging
from dotenv import load_dotenv


dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))
except FileNotFoundError:
    pass

DATABASE_FILENAME = os.getenv('DATABASE_FILENAME') or 'database.db'
PATH_NAME = os.getenv('DATABASE_PATH') or 'db'
DATABASE_PATH = os.path.join(dirname, '..', PATH_NAME)

SECRET_KEY = os.getenv('SECRET_KEY') or 'default-secret-key-template'

DATABASE_FILE_PATH = os.path.join(DATABASE_PATH, DATABASE_FILENAME)



