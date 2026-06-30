import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any
import joblib
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
SCALER_PATH = os.path.join(MODELS_DIR, "fitted_scaler.joblib")


def preprocess_data(data: pd.DataFrame, fit_scaler: bool = False) -> pd.DataFrame:
    """
    Perform feature engineering on raw environmental data.
    Adds interaction features, binary risk indicators, and rate-of-change proxies.
    """
    df = data.copy()

    # 1. Interaction: Rainfall × River Level (compound flood indicator)
    df['rainfall_river_inter'] = df['rainfall_mm'] * df['river_level_m']

    # 2. Binary Risk Indicators (threshold-based features)
    df['high_rainfall'] = (df['rainfall_mm'] > 50).astype(int)
    df['high_river'] = (df['river_level_m'] > 3.0).astype(int)

    # 3. Humidity-rainfall interaction (saturation indicator)
    df['humidity_rainfall'] = df['humidity_pct'] * df['rainfall_mm'] / 100.0

    # 4. Pressure-based features (if available)
    if 'pressure_hpa' in df.columns:
        df['pressure_hpa'] = df['pressure_hpa'].fillna(1013.25)
        df['low_pressure'] = (df['pressure_hpa'] < 1005).astype(int)
    else:
        df['pressure_hpa'] = 1013.25
        df['low_pressure'] = 0

    # 5. River discharge features (if available)
    if 'river_discharge_m3s' in df.columns:
        df['river_discharge_m3s'] = df['river_discharge_m3s'].fillna(0.0)
        df['high_discharge'] = (df['river_discharge_m3s'] > 5.0).astype(int)
    else:
        df['river_discharge_m3s'] = 0.0
        df['high_discharge'] = 0

    # Ensure consistent feature order
    feature_cols = [
        'rainfall_mm', 'river_level_m', 'humidity_pct', 'temperature_c',
        'wind_speed_kmh', 'pressure_hpa', 'river_discharge_m3s',
        'rainfall_river_inter', 'high_rainfall', 'high_river',
        'humidity_rainfall', 'low_pressure', 'high_discharge'
    ]

    # Only keep columns that exist
    feature_cols = [c for c in feature_cols if c in df.columns]
    df = df[feature_cols]

    # Fill any remaining NaN values
    df = df.fillna(0.0)

    return df


def get_scaler():
    """Returns a standard scaler for feature normalization."""
    return StandardScaler()
