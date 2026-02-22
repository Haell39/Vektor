import sqlite3
import json
import os
from datetime import datetime
import pandas as pd

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "vektor_history.db",
)


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            keywords TEXT,
            timeframe TEXT,
            geo TEXT,
            peak_term TEXT,
            peak_value INTEGER
        )
    """)
    conn.commit()
    return conn


def save_search(keywords: list, timeframe_label: str, geo_label: str, df: pd.DataFrame):
    try:
        peak_col = df.max().idxmax()
        peak_val = int(df[peak_col].max())
        c = _conn()
        c.execute(
            "INSERT INTO searches (created_at, keywords, timeframe, geo, peak_term, peak_value) VALUES (?,?,?,?,?,?)",
            (datetime.now().strftime("%d/%m/%Y %H:%M"), json.dumps(keywords), timeframe_label, geo_label, peak_col, peak_val),
        )
        c.commit()
        c.close()
    except Exception:
        pass


def get_history(limit: int = 30) -> pd.DataFrame:
    try:
        c = _conn()
        df = pd.read_sql(
            "SELECT * FROM searches ORDER BY created_at DESC LIMIT ?", c, params=(limit,)
        )
        c.close()
        df["keywords"] = df["keywords"].apply(json.loads)
        return df
    except Exception:
        return pd.DataFrame()


def clear_history():
    try:
        c = _conn()
        c.execute("DELETE FROM searches")
        c.commit()
        c.close()
    except Exception:
        pass
