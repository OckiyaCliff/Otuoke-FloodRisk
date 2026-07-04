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
        gap: 0.75rem;
        min-width: 0;
        padding: 0.6rem 0.8rem;
    }

    .weather-card:hover {
        transform: translateY(-2px);
    }

    .icon-container {
        flex-shrink: 0;
    }

    .icon {
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        background: var(--accent-blue-bg);
        width: clamp(36px, 8vw, 42px);
        height: clamp(36px, 8vw, 42px);
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
        font-size: clamp(0.65rem, 2vw, 0.75rem);
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
        font-size: clamp(1.1rem, 3vw, 1.35rem);
        font-weight: 700;
        color: var(--text-primary);
    }

    .unit {
        color: var(--text-secondary);
        font-size: clamp(0.7rem, 2vw, 0.8rem);
    }
</style>
