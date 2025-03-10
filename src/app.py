import logging
from flask import Flask
from config import SECRET_KEY

app = Flask(__name__)

# In production the secret key is fetched from env variables.
# In test environment default value can be used to enable Flask sessions.
# Flask sessions are needed for handling flash-messages. 
app.secret_key = SECRET_KEY

# Configure App to show debug logs
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
if app.debug:
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, handlers=[logging.StreamHandler()])
else:
    logging.basicConfig(format=FORMAT, level=logging.INFO)

# Setting up logger
logger = logging.getLogger(__name__)




from controller import view