<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { Alert } from '$lib/types';
    import StatusBadge from '$lib/components/StatusBadge.svelte';

    let alerts = $state<Alert[]>([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    async function loadAlerts() {
        try {
            alerts = await api.getAlerts();
        } catch (e) {
            error = "Failed to load alerts feed.";
        } finally {
            loading = false;
        }
    }

    onMount(loadAlerts);

    const getSeverityType = (severity: string) => {
        if (severity === 'High' || severity === 'Critical') return 'danger';
        if (severity === 'Medium') return 'warning';
        return 'safe';
    };
</script>

<div class="alerts-page">
    <header>
        <h1>Alerts Feed</h1>
        <p>Historical record of flood alerts issued by the system.</p>
    </header>

    {#if loading}
        <div class="loading-state">Loading alerts...</div>
    {:else if error}
        <div class="error-state glass-card">{error}</div>
    {:else if alerts.length === 0}
        <div class="empty-state glass-card">
            <p>No alerts have been issued yet. The system is currently reporting safe conditions.</p>
        </div>
    {:else}
        <div class="alerts-list">
            {#each alerts as alert}
                <div class="alert-item glass-card">
                    <div class="alert-header">
                        <StatusBadge text={alert.severity} type={getSeverityType(alert.severity)} />
                        <span class="timestamp">{new Date(alert.created_at).toLocaleString()}</span>
                    </div>
                    <p class="message">{alert.message}</p>
                    <div class="alert-footer">
                        <span>Channel: <strong>{alert.channel}</strong></span>
                        <span>Recipient: <strong>{alert.recipient}</strong></span>
                        <span class="status {alert.status}">Status: {alert.status}</span>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .alerts-page {
        padding: 1.5rem;
    }

    header {
        margin-bottom: 2rem;
    }

    .alerts-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .alert-item {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .alert-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .timestamp {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    .message {
        font-size: 1.125rem;
        font-weight: 500;
        color: var(--text-primary);
    }

    .alert-footer {
        display: flex;
        gap: 2rem;
        font-size: 0.75rem;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
        padding-top: 0.75rem;
        margin-top: 0.25rem;
    }

    .status.sent { color: var(--color-safe); }
    .status.failed { color: var(--color-danger); }

    .loading-state, .empty-state {
        text-align: center;
        padding: 4rem;
        color: var(--text-secondary);
    }
</style>
