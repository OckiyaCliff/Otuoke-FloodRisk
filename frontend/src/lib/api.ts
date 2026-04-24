import type { WeatherData, Prediction, Alert, User } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        }
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
}

export const api = {
    // Weather
    getLatestWeather: () => apiFetch<WeatherData>('/weather/latest/'),
    getWeatherHistory: (limit = 50) => apiFetch<WeatherData[]>(`/weather/?limit=${limit}`),

    // Predictions
    getLatestPrediction: () => apiFetch<Prediction>('/predictions/latest/'),
    getPredictionsHistory: (limit = 50) => apiFetch<Prediction[]>(`/predictions/?limit=${limit}`),

    // Alerts
    getAlerts: (limit = 50) => apiFetch<Alert[]>(`/alerts/?limit=${limit}`),

    // Users
    getUsers: () => apiFetch<User[]>('/users/'),
    registerUser: (userData: Partial<User>) => apiFetch<User>('/users/', {
        method: 'POST',
        body: JSON.stringify(userData)
    })
};
