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
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, date, name, distance, steps, calories FROM TRACKING_DATA")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        return columns, rows

    def add_entry(self, tracking_data: TrackingDataEntry) -> None:
        """A method to add tracking data entry

        Args:
            tracking_data (TrackingData): tracking data object
        """

        cursor = self._connection.cursor()
        cursor.execute('''INSERT INTO TRACKING_DATA
                    (date, name, distance, steps, calories) 
                    VALUES (?,?)''',
                       [tracking_data.date,
                        tracking_data.name,
                        tracking_data.distance,
                        tracking_data.steps,
                        tracking_data.calories]
                       )
        self._connection.commit()


default_tracking_data_repository = TrackingDataRepository(
    get_database_connection())
