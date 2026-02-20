import datetime

from server.infrastructure.interface.RunningNotionClient import RunningNotionClient
from server.infrastructure.interface.CyclingNotionClient import CyclingNotionClient
from server.infrastructure.interface.WeatherClient import WeatherClient
from server.presentation.dto.RunningResponse import RunningResponse
from server.presentation.dto.CyclingResponse import CyclingResponse
from typing import Optional
import re


class RunningService:

    def __init__(self):
        self.running_model = RunningNotionClient()
        self.ex_running_model = CyclingNotionClient()
        self.running_data = self.running_model.create_model()
        self.ex_running_data = self.ex_running_model.create_model()
        self.weather_data = WeatherClient()

    def preprocess_response_data(self):
        return {
            "running": self.preprocess_running_data(),
            "cycling": self.preprocess_cycling_data(),
            "weather": self.preprocess_weather_data()
        }

    def preprocess_running_data(self):
        response_data = {}
        for i in self.running_data:
            sec_time = self.preprocess_time(i.time)
            m_distance = self.km2m(i.distance)
            kcal = int(i.kcal)

            running = RunningResponse(sec_time, m_distance, kcal)
            response_data[i.date]=running.to_dict()

        return response_data

    def preprocess_cycling_data(self):
        response_data = {}
        for i in self.ex_running_data:
            sec_time = self.preprocess_time(i.time)
            kcal = int(i.kcal)

            cycling = CyclingResponse(sec_time, kcal)
            response_data[i.date] = cycling.to_dict()

        return response_data

    def preprocess_weather_data(self):
        current_datetime = datetime.datetime.now()
        base_date = current_datetime.strftime("%Y%m%d")
        base_time = current_datetime.strftime("%H00")
        response_data = self.weather_data.get_weather_data(base_date, base_time, 55, 127)

        return response_data

    def km2m(self, km_str: Optional[str]) -> Optional[float]:
        if km_str is None:
            return None
        try:
            return float(km_str) * 1000.0
        except ValueError:
            return None

    def preprocess_time(self, t: Optional[str]) -> Optional[int]:
        if not t:
            return None
        x = t.strip().lower()
        m = re.fullmatch(
            r'(?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?(?:(?P<s>\d+)s)?',
            x
        )
        if not m:
            return None

        h = int(m.group('h')) if m.group('h') else 0
        mm = int(m.group('m')) if m.group('m') else 0
        ss = int(m.group('s')) if m.group('s') else 0
        return h * 3600 + mm * 60 + ss
