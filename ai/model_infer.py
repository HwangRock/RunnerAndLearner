import json
from typing import Any, Dict

import torch.nn as nn


class GRUForecast(nn.Module):
    def __init__(self, in_feats: int, hidden: int, out_feats: int, num_layers: int, dropout: float):
        super().__init__()
        self.gru = nn.GRU(
            in_feats, hidden, num_layers=num_layers,
            batch_first=True, dropout=(dropout if num_layers > 1 else 0.0)
        )
        self.head = nn.Sequential(
            nn.Linear(hidden, 64), nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, out_feats),
        )

    def forward(self, x):  # x: (B,T,F)
        _, h = self.gru(x)  # (L,B,H)
        return self.head(h[-1])  # (B,out_feats)


def load_config(path: str = "config.json") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg


def build_model_from_config(config_path: str = "config.json") -> GRUForecast:
    cfg = load_config(config_path)
    return GRUForecast(
        in_feats=cfg["in_feats"],
        hidden=cfg["hidden"],
        out_feats=cfg["out_feats"],
        num_layers=cfg["num_layers"],
        dropout=float(cfg["dropout"]),
    )
