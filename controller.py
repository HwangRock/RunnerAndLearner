import re
from typing import List, Optional, Dict, Any
from model import Model


class Controller:
    def __init__(self):
        self.model = Model()
        self.data: List[List[Optional[str]]] = self.model.create_model()
        self.cleaned: Optional[List[Dict[str, Any]]] = None

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

    def calculate_velocity(self, distance_km_str: Optional[str], time_str: Optional[str]) -> Optional[float]:
        sec = self.preprocess_time(time_str)
        meters = self.km2m(distance_km_str)
        if sec and sec > 0 and meters is not None:
            return round(meters / sec, 3)
        return None

    def preprocess(self) -> List[Dict[str, Any]]:
        cleaned: List[Dict[str, Any]] = []
        for row in self.data:
            date, time_str, distance_km_str, kcal_str = (row + [None, None, None, None])[:4]

            time_sec = self.preprocess_time(time_str)
            try:
                distance_km = float(distance_km_str) if distance_km_str is not None else None
            except ValueError:
                distance_km = None

            try:
                kcal = int(kcal_str) if kcal_str is not None else None
            except ValueError:
                kcal = None

            velocity_mps = self.calculate_velocity(distance_km_str, time_str)

            cleaned.append({
                "date": date,
                "time_sec": time_sec,
                "distance_km": distance_km,
                "kcal": kcal,
                "velocity_mps": velocity_mps,
            })

        self.cleaned = cleaned
        return cleaned
