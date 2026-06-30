import joblib
import os
import pandas as pd
from typing import Dict, Any
from .preprocessing import preprocess_data
import logging

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
LATEST_MODEL_PATH = os.path.join(MODELS_DIR, "latest_model.joblib")

# In-memory model cache to avoid reloading from disk on every request
_cached_model = None
_cached_model_mtime = None


def _load_model():
    """Load model with in-memory caching. Only reloads if file has changed."""
    global _cached_model, _cached_model_mtime

    if not os.path.exists(LATEST_MODEL_PATH):
        return None

    current_mtime = os.path.getmtime(LATEST_MODEL_PATH)

    if _cached_model is None or _cached_model_mtime != current_mtime:
        logger.info("Loading ML model from disk (cache miss or model updated)")
        _cached_model = joblib.load(LATEST_MODEL_PATH)
        _cached_model_mtime = current_mtime
    
    return _cached_model


def get_prediction(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load the latest model (cached) and run inference on provided features.
    Returns risk_level, risk_score, confidence, and model_version.
    """
    model = _load_model()

    if model is None:
        return {"error": "Model not trained yet", "risk_level": "Unknown", "confidence": 0.0, "risk_score": 0.0}

    # Convert dict to DataFrame for preprocessing
    df = pd.DataFrame([input_data])
    X = preprocess_data(df)

    # Inference
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    # Get confidence for the predicted class
    class_idx = list(model.classes_).index(prediction)
    confidence = float(probabilities[class_idx])

    # Calculate a continuous risk_score (0.0 - 1.0)
    # Weighted average of class probabilities where higher-risk classes get more weight
    risk_weights = {"No Risk": 0.0, "Low": 0.25, "Medium": 0.5, "High": 0.75, "Critical": 1.0}
    risk_score = sum(
        probabilities[i] * risk_weights.get(cls, 0.0)
        for i, cls in enumerate(model.classes_)
    )

    # Get model version from file timestamp
    model_version = "2.0.0"
    try:
        mtime = os.path.getmtime(LATEST_MODEL_PATH)
        from datetime import datetime
        model_version = f"2.0.0-{datetime.fromtimestamp(mtime).strftime('%Y%m%d')}"
    except Exception:
        pass

    return {
        "risk_level": prediction,
        "risk_score": round(risk_score, 4),
        "confidence": confidence,
        "model_version": model_version
    }
