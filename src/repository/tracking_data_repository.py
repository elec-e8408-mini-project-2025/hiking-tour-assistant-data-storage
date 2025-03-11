from database_connection import get_database_connection
from entity.tracking_data import TrackingDataEntry
from twatch_controller.twatch_controller import Twatch

from app import logger

class TrackingDataRepository:
    """A class for managing data queries related to user objects
    """

    def __init__(self, connection) -> None:
        """A constructor for the class.

        Args:
            connection (sqlite3 object): an initialized database connection
        """
        self._connection = connection

    def fetch_device_data(self) -> tuple[str, str] | None:
        """method for fetching device data

        Returns:
            tuple[str, str]
            str: mac-address
            str: device-name
        """
        logger.debug("BEGIN")
        cursor = self._connection.cursor()
        res = cursor.execute('SELECT mac_address, device_name FROM HIKING_WATCH')
        ret_res = res.fetchone()

        if ret_res == None:
            return None

        mac_address = ret_res[0]
        device_name = ret_res[1]
        self._connection.commit()
        logger.debug("END")

        return [mac_address, device_name]
    
    def update_watch_data(self, mac_address, device_name):
        """Empty hiking_watch table and update new values

        Returns:
            None
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM HIKING_WATCH")
        cursor.execute('''INSERT INTO HIKING_WATCH
                    (mac_address, device_name) 
                    VALUES (?,?)''',
                       [mac_address, device_name]
                       )
        self._connection.commit()

    def fetch_all_tracking_data(self) -> tuple[list, list]:
        """method for fetching all tracking data

        Returns:
            tuple[list, list]
            list: columns for fetched data based on descriptions
            list: row data
        """
        logger.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, date, distance, steps, calories, avgspeed FROM TRACKING_DATA")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        logger.debug("END")
        return columns, rows

    def add_entry(self, tracking_data: TrackingDataEntry) -> None:
        """A method to add tracking data entry

        Args:
            tracking_data (TrackingData): tracking data object
        """

        logger.debug("BEGIN")
        logger.debug(f'Adding entry: {tracking_data}')
        cursor = self._connection.cursor()
        query = '''INSERT INTO TRACKING_DATA
                    (date, distance, steps, calories, avgspeed) 
                    VALUES (?, ?, ?, ?, ?)'''
        content = (\
                    tracking_data.date,\
                    tracking_data.distance,\
                    tracking_data.steps,\
                    tracking_data.calories,\
                    tracking_data.avg_speed\
                    )
        #print(content)
        cursor.execute(query,content)
        self._connection.commit()
        logger.debug("END")

    def top_entry_for_distance(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logger.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, date, MAX(distance) as distance, steps, calories, avgspeed FROM TRACKING_DATA''')

        row = cursor.fetchone()

        if not row:
            row = None

        logger.debug("END")
        return row
    
    def top_entry_for_speed(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logger.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, date, distance, MAX(avgspeed) as avgspeed, steps, calories FROM TRACKING_DATA''')

        row = cursor.fetchone()

        if not row:
            row = None

        logger.debug("END")
        return row
    
    def fetch_last_entry(self) -> tuple | None:
        """Get the entry with the longest distance
        """

        logger.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT id, MAX(date) as date, distance, avgspeed, steps, calories FROM TRACKING_DATA ORDER BY id DESC LIMIT 1''')

        row = cursor.fetchone()

        if not row:
            row = None

        logger.debug("END")
        return row
        
        
    

    def fetch_avg_data(self) -> tuple | None:

        logger.debug("BEGIN")
        cursor = self._connection.cursor()

        cursor.execute(
            '''SELECT
                IFNULL(AVG(distance),0) AS avg_distance,
                IFNULL(AVG(steps),0) AS avg_steps,
                IFNULL(AVG(calories),0) AS avg_calories,
                IFNULL (AVG(avgspeed),0) AS avg_avgspeed
                FROM TRACKING_DATA
            ''')
        
        row = cursor.fetchone()

        if not row:
            row = None

        logger.debug("END")
        return row
    

    def delete_hike(self, hikeid: int) -> None:

        logger.debug("BEGIN")
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                '''DELETE FROM TRACKING_DATA WHERE id= ? ''', (hikeid, ))
            
            self._connection.commit()
            logger.debug("END")
        except Exception as e:
            
            logger.error(f'Exception raised when deleting hike id {hikeid}: {e}')
            self._connection.rollback()
            raise

        
    

default_tracking_data_repository = TrackingDataRepository(
    get_database_connection())
