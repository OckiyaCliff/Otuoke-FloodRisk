import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering on raw environmental data.
    """
    # Create derived features
    # 1. Interaction: Rainfall * River Level
    data['rainfall_river_inter'] = data['rainfall_mm'] * data['river_level_m']
    
    # 2. Risk Indicators (Hypothetical thresholds for feature engineering)
    data['high_rainfall'] = (data['rainfall_mm'] > 50).astype(int)
    data['high_river'] = (data['river_level_m'] > 3.0).astype(int)
    
    return data


def get_scaler():
    """Returns a standard scaler for feature normalization."""
    return StandardScaler()
