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
        } catch (e) {
            console.error(e);
            error = "Failed to load real-time data. Pleas ensure backend is running.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadData();
        const interval = setInterval(loadData, 30000); // Refresh every 30s
        return () => clearInterval(interval);
    });
</script>

<div class="dashboard">
    <header class="header">
        <div>
            <h1>Otuoke Flood Monitoring</h1>
            <p class="subtitle">Real-time status for Federal University Otuoke campus and surroundings.</p>
        </div>
        <div class="last-updated">
            {#if weather}
                Last reading: {new Date(weather.recorded_at).toLocaleTimeString()}
            {/if}
        </div>
    </header>

    {#if loading}
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Fetching real-time environmental data...</p>
        </div>
    {:else if error}
        <div class="error-state glass-card">
            <span class="error-icon">⚠️</span>
            <p>{error}</p>
            <button onclick={loadData}>Retry</button>
        </div>
    {:else}
        <div class="dashboard-grid">
            <div class="main-column">
                <div class="weather-grid">
                    <WeatherCard label="Rainfall" value={weather?.rainfall_mm.toFixed(1) || 0} unit="mm" icon="🌧️" />
                    <WeatherCard label="River Level" value={weather?.river_level_m.toFixed(2) || 0} unit="m" icon="🌊" />
                    <WeatherCard label="Humidity" value={weather?.humidity_pct.toFixed(0) || 0} unit="%" icon="💧" />
                    <WeatherCard label="Temperature" value={weather?.temperature_c.toFixed(1) || 0} unit="°C" icon="🌡️" />
                </div>
            </div>
            
            <div class="side-column">
                {#if prediction}
                    <RiskGauge riskLevel={prediction.risk_level} confidence={prediction.confidence} />
                {/if}

                <div class="status-card glass-card">
                    <h3>System Status</h3>
                    <div class="status-list">
                        <div class="status-item">
                            <span>Sensors</span>
                            <span class="status-badge status-safe">Online</span>
                        </div>
                        <div class="status-item">
                            <span>ML Engine</span>
                            <span class="status-badge status-safe">Live</span>
                        </div>
                        <div class="status-item">
                            <span>Alert Service</span>
                            <span class="status-badge status-safe">Active</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .dashboard {
        padding: 1.5rem;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
    }

    .subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
    }

    .last-updated {
        color: var(--text-secondary);
        font-size: 0.875rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 340px;
        gap: 1.5rem;
    }

    .weather-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }

    .side-column {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .status-card h3 {
        font-size: 1.125rem;
        margin-bottom: 1.25rem;
    }

    .status-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 500;
    }

    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        color: var(--text-secondary);
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--border-color);
        border-top: 4px solid var(--accent-blue);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .error-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 3rem;
        max-width: 500px;
        margin: 2rem auto;
        text-align: center;
    }

    .error-icon { font-size: 3rem; }

    button {
        background: var(--accent-blue);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
    }

    @media (max-width: 1024px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        .side-column {
            order: -1;
        }
    }

    @media (max-width: 640px) {
        .weather-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
