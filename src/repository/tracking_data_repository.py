import logging
from database_connection import get_database_connection
from entity.tracking_data import TrackingDataEntry


class TrackingDataRepository:
    """A class for managing data queries related to user objects
    """

    def __init__(self, connection) -> None:
        """A constructor for the class.

        Args:
            connection (sqlite3 object): an initialized database connection
        """
        self._connection = connection

    def fetch_all_tracking_data(self) -> tuple[list, list]:
        """method for fetching all tracking data

        Returns:
            tuple[list, list]
            list: columns for fetched data based on descriptions
            list: row data
        """
        logging.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, date, distance, steps, calories, avgspeed FROM TRACKING_DATA")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        logging.debug("END")
        return columns, rows

    def add_entry(self, tracking_data: TrackingDataEntry) -> None:
        """A method to add tracking data entry

        Args:
            tracking_data (TrackingData): tracking data object
        """

        logging.debug("BEGIN")
        logging.debug(f'Adding entry: {tracking_data}')
        cursor = self._connection.cursor()
        cursor.execute('''INSERT INTO TRACKING_DATA
                    (date, name, distance, steps, calories) 
                    VALUES (?,?)''',
                       [tracking_data.date,
                        tracking_data.distance,
                        tracking_data.steps,
                        tracking_data.calories,
                        tracking_data.avg_speed]
                       )
        self._connection.commit()
        logging.debug("END")

    def top_entry_for_distance(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logging.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, date, MAX(distance) as distance, steps, calories, avgspeed FROM TRACKING_DATA''')

        row = cursor.fetchone()

        if not row:
            row = None

        logging.debug("END")
        return row
    
    def top_entry_for_speed(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logging.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, date, distance, MAX(avgspeed) as avgspeed, steps, calories FROM TRACKING_DATA''')

        row = cursor.fetchone()

        if not row:
            row = None

        logging.debug("END")
        return row
    
    def fetch_last_entry(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logging.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, MAX(date) as date, distance, avgspeed, steps, calories FROM TRACKING_DATA ORDER BY id DESC LIMIT 1''')

        row = cursor.fetchone()

        if not row:
            row = None

        logging.debug("END")
        return row
        
        
    

    def fetch_avg_data(self) -> tuple | None:

        logging.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT AVG(distance) AS avg_distance, AVG(steps) AS avg_steps, AVG(calories) AS avg_calories, AVG(avgspeed) AS avg_avgspeed FROM TRACKING_DATA''')
        
        row = cursor.fetchone()

        if not row:
            row = None

        logging.debug("END")
        return row
    

    def delete_hike(self, hikeid: int) -> None:

        logging.debug("BEGIN")
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                '''DELETE FROM TRACKING_DATA WHERE id= ? ''', (hikeid, ))
            
            self._connection.commit()
            logging.debug("END")
        except Exception as e:
            
            logging.error(f'Exception raised when deleting hike id {hikeid}: {e}')
            self._connection.rollback()
            raise

        
    

default_tracking_data_repository = TrackingDataRepository(
    get_database_connection())
