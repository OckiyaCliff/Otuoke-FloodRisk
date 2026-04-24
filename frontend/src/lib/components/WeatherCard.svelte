<script lang="ts">
    interface Props {
        label: string;
        value: string | number;
        unit: string;
        icon: string;
    }
    const { label, value, unit, icon }: Props = $props();
</script>

<div class="weather-card glass-card">
    <div class="icon">{icon}</div>
    <div class="content">
        <span class="label">{label}</span>
        <div class="value-container">
            <span class="value">{value}</span>
            <span class="unit">{unit}</span>
        </div>
    </div>
</div>

<style>
    .weather-card {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .weather-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }

    .icon {
        font-size: 2.5rem;
        background: rgba(255, 255, 255, 0.05);
        width: 64px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
    }

    .content {
        display: flex;
        flex-direction: column;
    }

    .label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .value {
        font-size: 1.75rem;
        font-weight: 700;
    }

    .unit {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-left: 0.25rem;
    }
</style>
