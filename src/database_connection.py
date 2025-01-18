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

    cursor.execute('''
        CREATE TABLE TRACKING_DATA (
            col1 TEXT,
            col2 TEXT
        )
    ''')

    conn.commit()

    logger.debug("END")


def initialize_database():
    """Calls a method to activate the object that enables database connection.

    Calls methods to delete and create tables to database.

    """

    logger.debug("BEGIN")

    if not os.path.exists(DATABASE_PATH):
        os.mkdir(DATABASE_PATH)

    print(f"DATABASE_PATH {DATABASE_PATH}")
    print(f"DATABSE FILE PATH {DATABASE_FILE_PATH}")

    conn = sqlite3.connect(DATABASE_FILE_PATH)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    conn.close()

    logger.debug("END")
