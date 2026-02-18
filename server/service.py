from model.running_repository import RunningRepository
from model.ex_running_repository import ExRunningRepository
from server.dto.runnning_dto import RunningDto
from server.dto.ex_running_dto import ExRunningDto
from typing import List, Optional, Dict, Any
import re


class RunningService:

    def __init__(self):
        self.running_model = RunningRepository()
        self.ex_running_model = ExRunningRepository()
        self.running_data = self.running_model.create_model()
        self.ex_running_data = self.ex_running_model.create_model()

    def preprocess_running_data(self):
        response_data = []
        for i in self.running_data:
            sec_time = self.preprocess_time(i.time)
            m_distance = self.km2m(i.distance)
            kcal = int(i.kcal)
            running = RunningDto(i.date, sec_time, m_distance, kcal)
            response_data.append(running)

        response_data.reverse()
        return response_data

    def preprocess_ex_running_data(self):
        response_data = []
        for i in self.ex_running_data:
            sec_time = self.preprocess_time(i.time)
            kcal = int(i.kcal)
            ex_running = ExRunningDto(i.date, i.name, sec_time, kcal)
            response_data.append(ex_running)

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
