import os
import requests


class WeatherClient:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

    def get_weather_data(self, base_date, base_time, nx, ny):
        params = {
            "serviceKey": self.api_key,
            "pageNo": "1",
            "numOfRows": "1000",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()
