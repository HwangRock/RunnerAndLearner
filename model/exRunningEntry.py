from dataclasses import dataclass


@dataclass
class ExRunningEntry:
    date: str
    name: str
    time: str
    kcal: str

    def to_dict(self):
        return {
            "date": self.date,
            "name": self.name,
            "time": self.time,
            "kcal": self.kcal
        }

    @classmethod
    def change(cls, props: dict, extractor):
        date = extractor(props.get("date"))
        name = extractor(props.get("name"))
        time = extractor(props.get("time"))
        kcal = extractor(props.get("kcal"))

        return cls(date=date, name=name, time=time, kcal=kcal)
