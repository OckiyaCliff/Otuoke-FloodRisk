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
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Loading alerts...</p>
        </div>
    {:else if error}
        <div class="error-state card">{error}</div>
    {:else if alerts.length === 0}
        <div class="empty-state card">
            <span class="empty-icon">✅</span>
            <p>No alerts have been issued. The system is currently reporting safe conditions.</p>
        </div>
    {:else}
        <div class="alerts-list">
            {#each alerts as alert}
                <div class="alert-item card">
                    <div class="alert-header">
                        <StatusBadge text={alert.severity} type={getSeverityType(alert.severity)} />
                        <span class="timestamp">{new Date(alert.created_at).toLocaleString()}</span>
                    </div>
                    <p class="message">{alert.message}</p>
                    <div class="alert-footer">
                        <span class="footer-item">
                            <span class="footer-label">Channel</span>
                            <strong>{alert.channel}</strong>
                        </span>
                        <span class="footer-item">
                            <span class="footer-label">Recipient</span>
                            <strong>{alert.recipient}</strong>
                        </span>
                        <span class="footer-item">
                            <span class="footer-label">Status</span>
                            <strong class="delivery-status" class:sent={alert.status === 'sent'} class:failed={alert.status === 'failed'}>{alert.status}</strong>
                        </span>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .alerts-page {
        padding: clamp(0.5rem, 2vw, 1rem) 0;
    }

    header {
        margin-bottom: clamp(1.25rem, 3vw, 2rem);
    }

    .alerts-list {
        display: flex;
        flex-direction: column;
        gap: 0.875rem;
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
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .timestamp {
        color: var(--text-muted);
        font-size: 0.8125rem;
    }

    .message {
        font-size: clamp(0.875rem, 2.5vw, 1rem);
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.5;
        white-space: pre-line;
    }

    .alert-footer {
        display: flex;
        flex-wrap: wrap;
        gap: clamp(0.75rem, 3vw, 2rem);
        font-size: 0.75rem;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
        padding-top: 0.75rem;
    }

    .footer-item {
        display: flex;
        flex-direction: column;
        gap: 0.125rem;
    }

    .footer-label {
        color: var(--text-muted);
        font-size: 0.6875rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .delivery-status { color: var(--text-secondary); }
    .delivery-status.sent { color: var(--color-safe); }
    .delivery-status.failed { color: var(--color-danger); }

    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 200px;
        justify-content: center;
        gap: 1rem;
        color: var(--text-secondary);
    }

    .empty-state {
        text-align: center;
        padding: clamp(2rem, 5vw, 4rem);
        color: var(--text-secondary);
    }

    .empty-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.75rem;
    }

    .error-state {
        text-align: center;
        padding: 2rem;
        color: var(--color-danger);
    }
</style>
