import os
import sqlite3
import logging
from config import DATABASE_FILE_PATH, DATABASE_PATH

logger = logging.getLogger(__name__)


def get_database_connection() -> sqlite3.Connection:
    """A method for returning the connection object in Singleton fashion

    TODO: Consider whether we want to improve thread safety. In that case we should
    open connection to database for each action separately instead of singleton-like 
    connection. This creates overhead but improves safety.

    Returns:
        connection (connect object): an object that enables the database connection.
    """

    logger.debug("BEGIN")

    if not os.path.exists(DATABASE_FILE_PATH):
        initialize_database()
    else:
        logger.debug(f'Connecting to existing database {DATABASE_FILE_PATH}')

    connection = sqlite3.connect(
        DATABASE_FILE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row

    logger.debug("END")

    return connection


def create_tables(conn):
    """Creates database tables for the application

    Args:
        connection (connect object): an object that enables the database connection.
    """
    logger.debug("BEGIN")
    cursor = conn.cursor()

    with open('schema.sql') as schema:
        cursor.executescript(schema.read())

    conn.commit()

    logger.debug("END")


def initialize_database():
    """Initializes the database if one does not exist
    """

    logger.debug("BEGIN")

    if not os.path.exists(DATABASE_PATH):
        os.mkdir(DATABASE_PATH)

    logger.debug(f'Database directory: {DATABASE_PATH}')
    logger.debug(f'Database filename: {DATABASE_FILE_PATH}')

    # If database does not yet exist, connect generates a new database
    conn = sqlite3.connect(DATABASE_FILE_PATH)
    conn.row_factory = sqlite3.Row
    
    logger.debug('Creating database from schema.sql')
    create_tables(conn)
    
    conn.close()

    logger.debug("END")
