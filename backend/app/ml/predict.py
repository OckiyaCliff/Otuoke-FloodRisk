import joblib
import os
import pandas as pd
from typing import Dict, Any
from .preprocessing import preprocess_data

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
LATEST_MODEL_PATH = os.path.join(MODELS_DIR, "latest_model.joblib")


def get_prediction(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load the latest model and run inference on provided features.
    """
    if not os.path.exists(LATEST_MODEL_PATH):
        return {"error": "Model not trained yet", "risk_level": "Unknown", "confidence": 0.0}
    
    model = joblib.load(LATEST_MODEL_PATH)
    
    # Convert dict to DataFrame for preprocessing
    df = pd.DataFrame([input_data])
    X = preprocess_data(df)
    
    # Inference
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    # Get confidence for the predicted class
    class_idx = list(model.classes_).index(prediction)
    confidence = float(probabilities[class_idx])
    
    return {
        "risk_level": prediction,
        "confidence": confidence,
        "model_version": "1.0.0"
    }
