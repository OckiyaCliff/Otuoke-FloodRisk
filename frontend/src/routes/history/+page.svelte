<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { WeatherData } from '$lib/types';

    let history = $state<WeatherData[]>([]);
    let loading = $state(true);

    onMount(async () => {
        try {
            history = await api.getWeatherHistory(30);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    const formatValue = (val: number) => val.toFixed(2);
</script>

<div class="history-page">
    <header>
        <h1>Historical Trends</h1>
        <p>Review environmental data from the last 30 readings.</p>
    </header>

    {#if loading}
        <p>Loading history...</p>
    {:else}
        <div class="table-container glass-card">
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Rainfall (mm)</th>
                        <th>River Level (m)</th>
                        <th>Humidity (%)</th>
                        <th>Temp (°C)</th>
                    </tr>
                </thead>
                <tbody>
                    {#each history as entry}
                        <tr>
                            <td>{new Date(entry.recorded_at).toLocaleTimeString()}</td>
                            <td>{formatValue(entry.rainfall_mm)}</td>
                            <td>{formatValue(entry.river_level_m)}</td>
                            <td>{entry.humidity_pct.toFixed(1)}</td>
                            <td>{entry.temperature_c.toFixed(1)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

<style>
    .history-page {
        padding: 1.5rem;
    }

    header {
        margin-bottom: 2rem;
    }

    .table-container {
        overflow-x: auto;
        padding: 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }

    th {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    td {
        padding: 1rem;
        border-bottom: 1px solid var(--border-color);
        font-size: 0.9375rem;
    }

    tr:hover td {
        background: rgba(255, 255, 255, 0.02);
    }
</style>
