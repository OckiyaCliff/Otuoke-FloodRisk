export interface WeatherData {
    id: string;
    rainfall_mm: number;
    river_level_m: number;
    humidity_pct: number;
    temperature_c: number;
    wind_speed_kmh: number;
    source: string;
    recorded_at: string;
    created_at: string;
}

export interface Prediction {
    id: string;
    weather_data_id: string;
    risk_level: 'No Risk' | 'Low' | 'Medium' | 'High' | 'Critical';
    confidence: number;
    model_version: string;
    created_at: string;
}

export interface Alert {
    id: string;
    prediction_id: string;
    severity: string;
    channel: string;
    status: string;
    recipient: string;
    message: string;
    sent_at: string | null;
    created_at: string;
}

export interface User {
    id: string;
    name: string;
    email: string;
    phone: string;
    is_active: boolean;
    preferences: any;
    created_at: string;
}
