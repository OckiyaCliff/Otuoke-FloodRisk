<script lang="ts">
    interface Props {
        riskLevel: 'No Risk' | 'Low' | 'Medium' | 'High' | 'Critical';
        confidence: number;
        riskScore?: number;
    }
    const { riskLevel, confidence, riskScore = 0 }: Props = $props();

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

    const isHighRisk = $derived(riskLevel === 'High' || riskLevel === 'Critical');
</script>

<div class="risk-gauge card" class:pulse-danger={isHighRisk}>
    <h3>Current Flood Risk</h3>
    <div class="gauge-container">
        <svg viewBox="0 0 100 55">
            <!-- Background arc -->
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="var(--bg-main)" stroke-width="8" stroke-linecap="round" />
            <!-- Active arc -->
            <path
                d="M 10 50 A 40 40 0 0 1 90 50"
                fill="none"
                stroke={getRiskColor(riskLevel)}
                stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="126"
                stroke-dashoffset={126 * (1 - confidence)}
                style="transition: stroke-dashoffset 1s ease-out, stroke 0.5s"
            />
        </svg>
        <div class="risk-info">
            <span class="level-text" style="color: {getRiskColor(riskLevel)}">{riskLevel}</span>
            <span class="confidence-text">Confidence: {(confidence * 100).toFixed(1)}%</span>
            {#if riskScore > 0}
                <span class="score-text">Risk Score: {(riskScore * 100).toFixed(0)}%</span>
            {/if}
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
        margin-top: 0.5rem;
    }

    svg {
        width: 100%;
        max-width: clamp(140px, 30vw, 180px);
        margin: 0 auto;
        display: block;
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
        font-size: clamp(1.2rem, 4vw, 1.6rem);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: -0.025em;
    }

    .confidence-text {
        color: var(--text-secondary);
        font-size: clamp(0.7rem, 2vw, 0.8rem);
        margin-top: -0.125rem;
    }

    .score-text {
        color: var(--text-muted);
        font-size: 0.7rem;
    }
</style>
