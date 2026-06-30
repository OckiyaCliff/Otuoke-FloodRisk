<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { WeatherData, Prediction } from '$lib/types';
    import WeatherCard from '$lib/components/WeatherCard.svelte';
    import RiskGauge from '$lib/components/RiskGauge.svelte';

    let weather = $state<WeatherData | null>(null);
    let prediction = $state<Prediction | null>(null);
    let loading = $state(true);
    let error = $state<string | null>(null);

    async function loadData() {
        try {
            const [w, p] = await Promise.all([
                api.getLatestWeather(),
                api.getLatestPrediction()
            ]);
            weather = w;
            prediction = p;
            error = null;
        } catch (e) {
            console.error(e);
            error = "Failed to load real-time data. Please ensure the backend is running.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadData();
        const interval = setInterval(loadData, 30000);
        return () => clearInterval(interval);
    });
</script>

<div class="dashboard">
    <header class="header">
        <div class="header-text">
            <h1>Otuoke Flood Monitoring</h1>
            <p class="subtitle">Real-time environmental monitoring for Federal University Otuoke and surroundings.</p>
        </div>
        {#if weather}
            <div class="last-updated">
                <span class="dot"></span>
                Live · {new Date(weather.recorded_at).toLocaleTimeString()}
            </div>
        {/if}
    </header>

    {#if loading}
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Fetching real-time environmental data...</p>
        </div>
    {:else if error}
        <div class="error-state card">
            <span class="error-icon">⚠️</span>
            <p>{error}</p>
            <button class="btn btn-primary" onclick={loadData}>Retry Connection</button>
        </div>
    {:else}
        <div class="dashboard-grid">
            <!-- Risk Gauge (top on mobile) -->
            <div class="risk-column">
                {#if prediction}
                    <RiskGauge
                        riskLevel={prediction.risk_level}
                        confidence={prediction.confidence}
                        riskScore={prediction.risk_score}
                    />
                {/if}

                <div class="status-card card">
                    <h3>System Status</h3>
                    <div class="status-list">
                        <div class="status-item">
                            <span>Data Source</span>
                            <span class="status-badge status-safe">Open-Meteo</span>
                        </div>
                        <div class="status-item">
                            <span>ML Engine</span>
                            <span class="status-badge status-safe">v2.0</span>
                        </div>
                        <div class="status-item">
                            <span>Alerts</span>
                            <span class="status-badge status-safe">Active</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Weather Cards -->
            <div class="weather-column">
                <div class="weather-grid">
                    <WeatherCard label="Rainfall" value={weather?.rainfall_mm.toFixed(1) || '0'} unit="mm" icon="🌧️" />
                    <WeatherCard label="River Level" value={weather?.river_level_m.toFixed(2) || '0'} unit="m" icon="🌊" />
                    <WeatherCard label="Humidity" value={weather?.humidity_pct.toFixed(0) || '0'} unit="%" icon="💧" />
                    <WeatherCard label="Temperature" value={weather?.temperature_c.toFixed(1) || '0'} unit="°C" icon="🌡️" />
                    <WeatherCard label="Wind Speed" value={weather?.wind_speed_kmh.toFixed(1) || '0'} unit="km/h" icon="💨" />
                    {#if weather?.pressure_hpa}
                        <WeatherCard label="Pressure" value={weather.pressure_hpa.toFixed(0)} unit="hPa" icon="🔵" />
                    {/if}
                </div>

                {#if weather?.river_discharge_m3s}
                    <div class="discharge-bar card">
                        <div class="discharge-info">
                            <span class="discharge-label">River Discharge</span>
                            <span class="discharge-value">{weather.river_discharge_m3s.toFixed(1)} m³/s</span>
                        </div>
                        <div class="discharge-track">
                            <div
                                class="discharge-fill"
                                style="width: {Math.min((weather.river_discharge_m3s / 15) * 100, 100)}%"
                            ></div>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>
    .dashboard {
        padding: clamp(0.5rem, 2vw, 1rem) 0;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-bottom: clamp(1.25rem, 3vw, 2rem);
    }

    .subtitle {
        font-size: clamp(0.8125rem, 2vw, 0.9375rem);
        margin-top: 0.25rem;
    }

    .last-updated {
        color: var(--color-safe);
        font-size: 0.8125rem;
        font-weight: 500;
        background: var(--color-safe-bg);
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        gap: 0.375rem;
        white-space: nowrap;
    }

    .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--color-safe);
        animation: pulse-dot 2s ease-in-out infinite;
    }

    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: 320px 1fr;
        gap: clamp(1rem, 3vw, 1.5rem);
    }

    .risk-column {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .weather-column {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .weather-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }

    .status-card h3 {
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .status-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 500;
        font-size: 0.875rem;
    }

    /* Discharge bar */
    .discharge-bar {
        padding: 1rem clamp(1rem, 3vw, 1.5rem);
    }

    .discharge-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.625rem;
    }

    .discharge-label {
        color: var(--text-secondary);
        font-size: 0.8125rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .discharge-value {
        font-weight: 700;
        font-size: 1rem;
        color: var(--accent-blue);
    }

    .discharge-track {
        width: 100%;
        height: 8px;
        background: var(--bg-main);
        border-radius: 4px;
        overflow: hidden;
    }

    .discharge-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-blue), var(--color-warning));
        border-radius: 4px;
        transition: width 1s ease-out;
    }

    /* Loading and error states */
    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 300px;
        color: var(--text-secondary);
        gap: 1rem;
    }

    .error-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: clamp(2rem, 5vw, 3rem);
        max-width: 420px;
        margin: 2rem auto;
        text-align: center;
    }

    .error-icon { font-size: 2.5rem; }

    /* Responsive */
    @media (max-width: 1024px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        .risk-column {
            order: -1;
        }
    }

    @media (max-width: 640px) {
        .weather-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
