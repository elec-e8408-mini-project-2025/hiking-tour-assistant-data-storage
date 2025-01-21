class TrackingDataEntry:
    """TODO: add docstring
    """

    def __init__(
            self,
            date: str,
            name: str,
            distance: float,
            steps: int,
            calories: float
    ):
        self.date = date
        self.name = name
        self.distance = distance
        self.steps = steps
        self.calories = calories
