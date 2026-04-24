<script lang="ts">
    interface Props {
        riskLevel: 'No Risk' | 'Low' | 'Medium' | 'High' | 'Critical';
        confidence: number;
    }
    const { riskLevel, confidence }: Props = $props();

    const getStatusClass = (level: string) => {
        switch (level) {
            case 'No Risk': return 'status-safe';
            case 'Low': return 'status-safe';
            case 'Medium': return 'status-warning';
            case 'High': return 'status-danger';
            case 'Critical': return 'status-danger';
            default: return '';
        }
    };

    const getRiskColor = (level: string) => {
        switch (level) {
            case 'No Risk': return 'var(--color-safe)';
            case 'Low': return '#86efac';
            case 'Medium': return 'var(--color-warning)';
            case 'High': return 'var(--color-danger)';
            case 'Critical': return 'var(--color-critical)';
            default: return 'var(--text-secondary)';
        }
    };
</script>

<div class="risk-gauge glass-card">
    <h3>Current Flood Risk</h3>
    <div class="gauge-container">
        <svg viewBox="0 0 100 50">
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#1e293b" stroke-width="8" stroke-linecap="round" />
            <path 
                d="M 10 50 A 40 40 0 0 1 90 50" 
                fill="none" 
                stroke={getRiskColor(riskLevel)} 
                stroke-width="8" 
                stroke-linecap="round" 
                stroke-dasharray="126"
                stroke-dashoffset={126 * (1 - confidence)}
                style="transition: stroke-dashoffset 1s ease-out, stroke 1s"
            />
        </svg>
        <div class="risk-info">
            <span class="level-text" style="color: {getRiskColor(riskLevel)}">{riskLevel}</span>
            <span class="confidence">Confidence: {(confidence * 100).toFixed(1)}%</span>
        </div>
    </div>
</div>

<style>
    .risk-gauge {
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .gauge-container {
        position: relative;
        margin-top: 1rem;
    }

    svg {
        width: 100%;
        max-width: 250px;
        margin: 0 auto;
    }

    .risk-info {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .level-text {
        font-size: 2rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: -0.025em;
    }

    .confidence {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-top: -0.25rem;
    }
</style>
