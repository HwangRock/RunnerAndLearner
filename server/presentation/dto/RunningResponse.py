class RunningResponse:
    def __init__(self, time: int, distance: float, kcal: int):
        self.time = time
        self.distance = distance
        self.kcal = kcal

    def to_dict(self):
        return {
            "time": self.time,
            "distance": self.distance,
            "kcal": self.kcal
        }