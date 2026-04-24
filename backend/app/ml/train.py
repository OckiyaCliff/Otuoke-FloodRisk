import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime
from .preprocessing import preprocess_data

# Ensure models directory exists
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)


def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic data for Otuoke flood prediction training.
    """
    np.random.seed(42)
    
    rainfall = np.random.uniform(0, 150, n_samples)
    river_level = np.random.uniform(0.5, 5.0, n_samples)
    humidity = np.random.uniform(40, 100, n_samples)
    temp = np.random.uniform(22, 35, n_samples)
    wind = np.random.uniform(0, 30, n_samples)
    
    # Simple logic for risk labelling:
    # High risk if rainfall > 100 and river > 3.5
    # Medium risk if rainfall > 60 or river > 2.5
    risk_scores = (rainfall * 0.5) + (river_level * 10) + (humidity * 0.1)
    
    risk_labels = []
    for score in risk_scores:
        if score > 80:
            risk_labels.append("High")
        elif score > 50:
            risk_labels.append("Medium")
        elif score > 25:
            risk_labels.append("Low")
        else:
            risk_labels.append("No Risk")
            
    df = pd.DataFrame({
        'rainfall_mm': rainfall,
        'river_level_m': river_level,
        'humidity_pct': humidity,
        'temperature_c': temp,
        'wind_speed_kmh': wind,
        'target': risk_labels
    })
    
    return df


def train_model():
    """
    Train a Random Forest classifier on synthetic data and save it.
    """
    print("Generating synthetic training data...")
    df = generate_synthetic_data()
    
    print("Preprocessing data...")
    X = preprocess_data(df.drop('target', axis=1))
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(MODELS_DIR, f"flood_model_{timestamp}.joblib")
    latest_path = os.path.join(MODELS_DIR, "latest_model.joblib")
    
    joblib.dump(model, model_path)
    joblib.dump(model, latest_path)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained. Accuracy: {accuracy:.4f}")
    print(f"Model saved to {model_path}")
    
    return model_path


if __name__ == "__main__":
    train_model()
