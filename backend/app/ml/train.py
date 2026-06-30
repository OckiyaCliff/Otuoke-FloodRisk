import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
import httpx
from datetime import datetime
from .preprocessing import preprocess_data

# Ensure models directory exists
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Otuoke coordinates
OTUOKE_LAT = 4.7833
OTUOKE_LON = 6.3333


def fetch_historical_weather(start_date: str = "2020-01-01", end_date: str = "2024-12-31") -> pd.DataFrame:
    """
    Fetch real historical weather data from Open-Meteo Archive API for Otuoke.
    Falls back to enhanced synthetic data if API is unavailable.
    """
    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": OTUOKE_LAT,
            "longitude": OTUOKE_LON,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,wind_speed_10m_max,surface_pressure_max",
            "timezone": "Africa/Lagos"
        }

        response = httpx.get(url, params=params, timeout=60.0)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]
        df = pd.DataFrame({
            "date": pd.to_datetime(daily["time"]),
            "rainfall_mm": daily["precipitation_sum"],
            "temperature_c": [(mx + mn) / 2 for mx, mn in zip(daily["temperature_2m_max"], daily["temperature_2m_min"])],
            "humidity_pct": daily["relative_humidity_2m_max"],
            "wind_speed_kmh": daily["wind_speed_10m_max"],
            "pressure_hpa": daily.get("surface_pressure_max", [1013.25] * len(daily["time"])),
        })

        # Fill NaN values
        df = df.fillna(method='ffill').fillna(method='bfill').fillna(0)

        print(f"Fetched {len(df)} days of historical weather data from Open-Meteo.")
        return df

    except Exception as e:
        print(f"Open-Meteo Archive API unavailable ({e}). Using enhanced synthetic data.")
        return generate_enhanced_synthetic_data()


def fetch_historical_flood(start_date: str = "2020-01-01", end_date: str = "2024-12-31") -> pd.DataFrame:
    """
    Fetch historical river discharge data from Open-Meteo Flood API.
    """
    try:
        url = "https://flood-api.open-meteo.com/v1/flood"
        params = {
            "latitude": OTUOKE_LAT,
            "longitude": OTUOKE_LON,
            "daily": "river_discharge",
            "start_date": start_date,
            "end_date": end_date,
        }

        response = httpx.get(url, params=params, timeout=60.0)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]
        df = pd.DataFrame({
            "date": pd.to_datetime(daily["time"]),
            "river_discharge_m3s": daily["river_discharge"],
        })

        df = df.fillna(0)
        print(f"Fetched {len(df)} days of river discharge data from Open-Meteo Flood API.")
        return df

    except Exception as e:
        print(f"Open-Meteo Flood API unavailable ({e}). Using synthetic river data.")
        return None


def generate_enhanced_synthetic_data(n_samples=2000) -> pd.DataFrame:
    """
    Generate enhanced synthetic data calibrated to Otuoke's tropical climate.
    Otuoke: ~4.78°N, tropical, avg temp 25-33°C, heavy rainfall May-Oct.
    """
    np.random.seed(42)

    # Seasonal patterns: two halves — dry (Nov-Apr) and wet (May-Oct)
    months = np.random.choice(range(1, 13), n_samples)
    is_wet_season = np.isin(months, [5, 6, 7, 8, 9, 10])

    rainfall = np.where(
        is_wet_season,
        np.random.exponential(40, n_samples),  # Wet season: heavier rains
        np.random.exponential(5, n_samples)     # Dry season: light rains
    )
    rainfall = np.clip(rainfall, 0, 250)

    river_level = np.where(
        is_wet_season,
        np.random.normal(3.0, 1.0, n_samples),
        np.random.normal(1.5, 0.5, n_samples)
    )
    river_level = np.clip(river_level, 0.3, 8.0)

    humidity = np.where(
        is_wet_season,
        np.random.normal(85, 5, n_samples),
        np.random.normal(65, 10, n_samples)
    )
    humidity = np.clip(humidity, 30, 100)

    temp = np.random.normal(28, 3, n_samples)
    temp = np.clip(temp, 22, 38)

    wind = np.random.exponential(8, n_samples)
    wind = np.clip(wind, 0, 40)

    pressure = np.random.normal(1012, 5, n_samples)
    pressure = np.clip(pressure, 995, 1025)

    df = pd.DataFrame({
        "rainfall_mm": rainfall,
        "river_level_m": river_level,
        "humidity_pct": humidity,
        "temperature_c": temp,
        "wind_speed_kmh": wind,
        "pressure_hpa": pressure,
    })

    return df


def derive_risk_labels(df: pd.DataFrame, discharge_df: pd.DataFrame = None) -> pd.Series:
    """
    Derive flood risk labels using a weighted multi-factor scoring system.
    Calibrated to Otuoke's flood-prone geography (Niger Delta lowland).
    """
    # Composite risk score (0-100 scale)
    score = (
        df['rainfall_mm'] * 0.35 +          # Rainfall is primary driver
        df['river_level_m'] * 8.0 +          # River level is critical
        df['humidity_pct'] * 0.08 +           # High humidity = saturated ground
        (1013 - df.get('pressure_hpa', 1013)) * 0.5 +  # Low pressure = storms
        df.get('river_discharge_m3s', 0) * 1.5  # Upstream discharge
    )

    labels = pd.cut(
        score,
        bins=[-np.inf, 20, 40, 65, 85, np.inf],
        labels=["No Risk", "Low", "Medium", "High", "Critical"]
    )

    return labels


def train_model():
    """
    Train a Random Forest classifier on real or enhanced synthetic data and save it.
    """
    print("=" * 60)
    print("OTUOKE FLOODWATCH — MODEL TRAINING")
    print("=" * 60)

    # Step 1: Fetch historical weather data
    print("\n[1/5] Fetching historical weather data...")
    weather_df = fetch_historical_weather()

    # Step 2: Fetch historical flood data
    print("[2/5] Fetching historical river discharge data...")
    flood_df = fetch_historical_flood()

    # Step 3: Merge weather + flood data (if both available)
    if flood_df is not None and 'date' in weather_df.columns and 'date' in flood_df.columns:
        df = weather_df.merge(flood_df, on='date', how='left')
        df['river_discharge_m3s'] = df['river_discharge_m3s'].fillna(0)
    else:
        df = weather_df
        if 'river_discharge_m3s' not in df.columns:
            df['river_discharge_m3s'] = 0.0

    # Synthesize river_level_m from discharge if not present
    if 'river_level_m' not in df.columns:
        df['river_level_m'] = np.clip(df['river_discharge_m3s'] * 0.5 + np.random.normal(1.5, 0.3, len(df)), 0.3, 8.0)

    # Drop date column for training
    if 'date' in df.columns:
        df = df.drop('date', axis=1)

    # Step 4: Derive risk labels
    print("[3/5] Deriving risk labels...")
    df['target'] = derive_risk_labels(df)
    df = df.dropna(subset=['target'])

    print(f"    Training samples: {len(df)}")
    print(f"    Class distribution:\n{df['target'].value_counts().to_string()}")

    # Step 5: Preprocess and train
    print("[4/5] Preprocessing and training Random Forest model...")
    X = preprocess_data(df.drop('target', axis=1))
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(MODELS_DIR, f"flood_model_{timestamp}.joblib")
    latest_path = os.path.join(MODELS_DIR, "latest_model.joblib")

    joblib.dump(model, model_path)
    joblib.dump(model, latest_path)

    accuracy = model.score(X_test, y_test)

    print(f"\n[5/5] Training complete!")
    print(f"    Accuracy: {accuracy:.4f}")
    print(f"    Model saved: {model_path}")
    print(f"    Feature importance (top 5):")

    importances = sorted(
        zip(X.columns, model.feature_importances_),
        key=lambda x: x[1], reverse=True
    )
    for feat, imp in importances[:5]:
        print(f"      {feat}: {imp:.4f}")

    print("=" * 60)

    return model_path


if __name__ == "__main__":
    train_model()
