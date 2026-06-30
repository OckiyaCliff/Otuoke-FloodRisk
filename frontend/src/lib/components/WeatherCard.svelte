<script lang="ts">
    interface Props {
        label: string;
        value: string | number;
        unit: string;
        icon: string;
    }
    const { label, value, unit, icon }: Props = $props();
</script>

<div class="weather-card card">
    <div class="icon-container">
        <span class="icon">{icon}</span>
    </div>
    <div class="content">
        <span class="label">{label}</span>
        <div class="value-row">
            <span class="value">{value}</span>
            <span class="unit">{unit}</span>
        </div>
    </div>
</div>

<style>
    .weather-card {
        display: flex;
        align-items: center;
        gap: clamp(0.75rem, 3vw, 1.25rem);
        min-width: 0;
    }

    .weather-card:hover {
        transform: translateY(-2px);
    }

    .icon-container {
        flex-shrink: 0;
    }

    .icon {
        font-size: clamp(1.75rem, 4vw, 2.25rem);
        background: var(--accent-blue-bg);
        width: clamp(48px, 10vw, 60px);
        height: clamp(48px, 10vw, 60px);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--radius-md);
    }

    .content {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .label {
        color: var(--text-muted);
        font-size: clamp(0.6875rem, 2vw, 0.8125rem);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .value-row {
        display: flex;
        align-items: baseline;
        gap: 0.25rem;
    }

    .value {
        font-size: clamp(1.25rem, 4vw, 1.625rem);
        font-weight: 700;
        color: var(--text-primary);
    }

    .unit {
        color: var(--text-secondary);
        font-size: clamp(0.75rem, 2vw, 0.875rem);
    }
</style>
