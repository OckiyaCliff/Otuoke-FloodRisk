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

    // Group entries by date for better readability
    function groupByDate(entries: WeatherData[]) {
        const groups: Record<string, WeatherData[]> = {};
        for (const entry of entries) {
            const date = new Date(entry.recorded_at).toLocaleDateString('en-NG', {
                weekday: 'short', day: 'numeric', month: 'short', year: 'numeric'
            });
            if (!groups[date]) groups[date] = [];
            groups[date].push(entry);
        }
        return groups;
    }
</script>

<div class="history-page">
    <header>
        <h1>Historical Trends</h1>
        <p>Environmental data from the last 30 readings.</p>
    </header>

    {#if loading}
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Loading history...</p>
        </div>
    {:else if history.length === 0}
        <div class="empty-state card">
            <p>No historical data available yet.</p>
        </div>
    {:else}
        <!-- Card view for mobile -->
        <div class="card-view">
            {#each Object.entries(groupByDate(history)) as [date, entries]}
                <h3 class="date-header">{date}</h3>
                <div class="entry-cards">
                    {#each entries as entry}
                        <div class="entry-card card">
                            <div class="entry-time">{new Date(entry.recorded_at).toLocaleTimeString()}</div>
                            <div class="entry-metrics">
                                <div class="metric">
                                    <span class="metric-icon">🌧️</span>
                                    <span class="metric-val">{formatValue(entry.rainfall_mm)}</span>
                                    <span class="metric-unit">mm</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-icon">🌊</span>
                                    <span class="metric-val">{formatValue(entry.river_level_m)}</span>
                                    <span class="metric-unit">m</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-icon">💧</span>
                                    <span class="metric-val">{entry.humidity_pct.toFixed(0)}</span>
                                    <span class="metric-unit">%</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-icon">🌡️</span>
                                    <span class="metric-val">{entry.temperature_c.toFixed(1)}</span>
                                    <span class="metric-unit">°C</span>
                                </div>
                                {#if entry.pressure_hpa}
                                    <div class="metric">
                                        <span class="metric-icon">🔵</span>
                                        <span class="metric-val">{entry.pressure_hpa.toFixed(0)}</span>
                                        <span class="metric-unit">hPa</span>
                                    </div>
                                {/if}
                            </div>
                            <div class="entry-source">Source: {entry.source}</div>
                        </div>
                    {/each}
                </div>
            {/each}
        </div>

        <!-- Table view for desktop -->
        <div class="table-view">
            <div class="table-container card">
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Rainfall (mm)</th>
                            <th>River (m)</th>
                            <th>Humidity (%)</th>
                            <th>Temp (°C)</th>
                            <th>Pressure (hPa)</th>
                            <th>Source</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each history as entry}
                            <tr>
                                <td class="time-col">{new Date(entry.recorded_at).toLocaleString()}</td>
                                <td>{formatValue(entry.rainfall_mm)}</td>
                                <td>{formatValue(entry.river_level_m)}</td>
                                <td>{entry.humidity_pct.toFixed(1)}</td>
                                <td>{entry.temperature_c.toFixed(1)}</td>
                                <td>{entry.pressure_hpa?.toFixed(0) || '—'}</td>
                                <td><span class="source-badge">{entry.source}</span></td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    {/if}
</div>

<style>
    .history-page {
        padding: clamp(0.5rem, 2vw, 1rem) 0;
    }

    header {
        margin-bottom: clamp(1.25rem, 3vw, 2rem);
    }

    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 200px;
        gap: 1rem;
        color: var(--text-secondary);
    }

    .empty-state {
        text-align: center;
        padding: 3rem;
        color: var(--text-secondary);
    }

    /* Card view (mobile) */
    .card-view { display: none; }

    .date-header {
        color: var(--text-secondary);
        font-size: 0.8125rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid var(--border-color);
    }

    .date-header:first-child {
        margin-top: 0;
    }

    .entry-cards {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .entry-card {
        padding: 0.875rem;
    }

    .entry-time {
        font-weight: 600;
        font-size: 0.875rem;
        color: var(--accent-blue);
        margin-bottom: 0.5rem;
    }

    .entry-metrics {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    .metric {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.875rem;
    }

    .metric-icon { font-size: 0.875rem; }
    .metric-val { font-weight: 600; }
    .metric-unit { color: var(--text-muted); font-size: 0.75rem; }

    .entry-source {
        margin-top: 0.5rem;
        font-size: 0.6875rem;
        color: var(--text-muted);
    }

    /* Table view (desktop) */
    .table-view { display: block; }

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
        background: rgba(255, 255, 255, 0.03);
        padding: 0.875rem 1rem;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        white-space: nowrap;
    }

    td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
        font-size: 0.875rem;
    }

    .time-col {
        white-space: nowrap;
        color: var(--text-secondary);
    }

    tr:hover td {
        background: rgba(37, 99, 235, 0.04);
    }

    .source-badge {
        background: var(--accent-blue-bg);
        color: var(--accent-blue);
        padding: 0.125rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Responsive: show cards on mobile, table on desktop */
    @media (max-width: 768px) {
        .card-view { display: block; }
        .table-view { display: none; }
    }
</style>
