import os
import requests
from dotenv import load_dotenv


class ExRunningModel:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("NOTION_EXDB_ID")
        self.api_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def extract_text(self, prop: dict):
        if not prop:
            return None
        t = prop["type"]
        arr = prop.get(t, [])
        if arr:
            return "".join([x.get("plain_text", "") for x in arr])
        return None

    def fetch_all_rows(self):
        results = []
        payload = {}
        while True:
            r = requests.post(self.api_url, headers=self.headers, json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()
            results.extend(data.get("results", []))
            if data.get("has_more"):
                payload = {"start_cursor": data.get("next_cursor")}
            else:
                break
        return results

    def create_model(self):
        data = []
        rows = self.fetch_all_rows()
        for row in rows:
            props = row["properties"]

            date = self.extract_text(props.get("date"))
            name = self.extract_text(props.get("name"))
            time = self.extract_text(props.get("time"))
            kcal = self.extract_text(props.get("kcal"))

            first = [date, name, time, kcal]
            data.append(first)

        return list(reversed(data))
