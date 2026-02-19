from dataclasses import dataclass


@dataclass
class RunningEntry:
    date: str
    time: str
    distance: str
    kcal: str

    def to_dict(self):
        return {
            "date": self.date,
            "time": self.time,
            "distance": self.distance,
            "kcal": self.kcal
        }

    @classmethod
    def change(cls, props: dict, extractor):
        date = extractor(props.get("date"))
        time = extractor(props.get("time"))
        distance = extractor(props.get("distance"))
        kcal = extractor(props.get("kcal"))

        return cls(date=date, time=time, distance=distance, kcal=kcal)
