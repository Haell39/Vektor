import numpy as np
import pandas as pd


def forecast_trend(series: pd.Series, periods: int = 90) -> pd.DataFrame | None:
    if len(series) < 12:
        return None

    y = series.values.astype(float)
    x = np.arange(len(y))

    coeffs = np.polyfit(x, y, 2)
    trend_fn = np.poly1d(coeffs)
    residuals = y - trend_fn(x)

    season_len = min(52, max(7, len(y) // 3))
    seasonal_pattern = np.array([
        np.mean(residuals[i::season_len]) for i in range(season_len)
    ])

    future_x = np.arange(len(y), len(y) + periods)
    trend_future = trend_fn(future_x)
    seasonal_future = np.array([seasonal_pattern[i % season_len] for i in range(periods)])
    yhat = np.clip(trend_future + seasonal_future, 0, 100)

    base_std = np.std(residuals)
    uncertainty = base_std * (1 + np.linspace(0, 1.2, periods))

    try:
        freq = pd.infer_freq(series.index) or "W"
    except Exception:
        freq = "W"

    future_dates = pd.date_range(start=series.index[-1], periods=periods + 1, freq=freq)[1:]

    return pd.DataFrame({
        "yhat": yhat,
        "yhat_lower": np.clip(yhat - uncertainty, 0, 100),
        "yhat_upper": np.clip(yhat + uncertainty, 0, 100),
    }, index=future_dates)
