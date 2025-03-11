class TrackingDataEntry:
    """TODO: add docstring
    """

    def __init__(
            self,
            date: str,
            avg_speed: float,
            distance: float,
            steps: int,
            calories: float
    ):
        self.date = date
        self.avg_speed = avg_speed
        self.distance = distance
        self.steps = steps
        self.calories = calories



    def __str__(self):
        return f'{self.date}: {self.distance} km at {self.avg_speed} km/h, with {self.steps} steps and {self.calories} kcal burned'
