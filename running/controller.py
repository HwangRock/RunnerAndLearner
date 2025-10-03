import re
from typing import List, Optional, Dict, Any
import joblib
from model.running_repository import RunningRepository
import torch
import numpy as np
from ai.model_infer import load_config, build_model_from_config
import os


class Controller:
    def __init__(self):
        self.model = RunningRepository()
        self.data: List[List[Optional[str]]] = self.model.create_model()
        self.cleaned: Optional[List[Dict[str, Any]]] = None

        self.cfg = load_config("../ai/config.json")
        self.lookback = self.cfg["lookback"]
        self.model_path = self.cfg["model_path"]
        self.scaler_path = self.cfg["scaler_path"]

        if os.path.exists(self.scaler_path):
            try:
                self.scaler = joblib.load(self.scaler_path)
            except Exception as e:
                print(f"[warn] failed to load scaler: {e}")
                self.scaler = None
        else:
            print(f"[warn] scaler file not found: {self.scaler_path}")
            self.scaler = None

        if os.path.exists(self.model_path):
            try:
                self.rnn = build_model_from_config("../ai/config.json")
                ckpt = torch.load(self.model_path, map_location="cpu", weights_only=True)
                if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
                    state = ckpt["model_state_dict"]
                else:
                    state = ckpt
                missing, unexpected = self.rnn.load_state_dict(state, strict=False)
                if missing or unexpected:
                    print("[warn] missing:", missing, "unexpected:", unexpected)
                self.rnn.eval()
            except Exception as e:
                print(f"[warn] failed to load model: {e}")
                self.rnn = None
        else:
            print(f"[warn] model file not found: {self.model_path}")
            self.rnn = None

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
            date = getattr(row, "date", None)
            time_str = getattr(row, "time", None)
            distance_km_str = getattr(row, "distance", None)
            kcal_str = getattr(row, "kcal", None)

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

    def predict_next(self):
        if self.rnn is None:
            print("[warn] no model loaded, skip prediction")
            return None

        if not self.cleaned:
            return None

        X_all = np.array([
            [
                row["time_sec"] if row["time_sec"] is not None else 0.0,
                row["velocity_mps"] if row["velocity_mps"] is not None else 0.0,
                row["kcal"] if row["kcal"] is not None else 0.0,
            ]
            for row in self.cleaned
        ], dtype=np.float32)

        if len(X_all) < self.lookback:
            return None

        seq = X_all[-self.lookback:]

        if self.scaler is not None:
            seq_scaled = self.scaler.transform(seq)
        else:
            print("[warn] scaler is None, using raw values")
            seq_scaled = seq

        x = torch.from_numpy(seq_scaled).unsqueeze(0)
        with torch.no_grad():
            y = self.rnn(x).cpu().numpy().ravel()

        return {
            "pred_distance_km": float(y[0]),
            "pred_time_sec": float(y[1]),
            "pred_kcal": float(y[2]),
        }
