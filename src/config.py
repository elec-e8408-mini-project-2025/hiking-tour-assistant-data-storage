import os
import logging
from dotenv import load_dotenv

# Get the absolute path
dirname = os.path.dirname(__file__)


# Try to load enviromental variables. In case env file is not found
# default values will be used instead
try:
    load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))
except FileNotFoundError:
    pass

# Set global variables from env file or by using default values
DATABASE_FILENAME = os.getenv('DATABASE_FILENAME') or 'database.db'
PATH_NAME = os.getenv('DATABASE_PATH') or 'db'
DATABASE_PATH = os.path.join(dirname, '..', PATH_NAME)
DATABASE_FILE_PATH = os.path.join(DATABASE_PATH, DATABASE_FILENAME)

# Secret key is required for enabling sessions in Flask
# In the web application sessions are needed only for showing
# flash messages. In a dev environment the default value may be used.
# In production, a proper secret key MUST be used and it MUST be properly
# secured.
SECRET_KEY = os.getenv('SECRET_KEY') or 'default-secret-key-template'





