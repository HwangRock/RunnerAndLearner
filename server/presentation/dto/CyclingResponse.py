class CyclingResponse:
    def __init__(self, time: int, kcal: int):
        self.time = time
        self.kcal = kcal

    def to_dict(self):
        return {
            "time": self.time,
            "kcal": self.kcal
        }
