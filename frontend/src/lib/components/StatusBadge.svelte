<script lang="ts">
    interface Props {
        text: string;
        type?: 'safe' | 'warning' | 'danger' | 'info';
    }
    const { text, type = 'info' }: Props = $props();

    const getBadgeClass = (type: string) => {
        switch (type) {
            case 'safe': return 'status-safe';
            case 'warning': return 'status-warning';
            case 'danger': return 'status-danger';
            case 'info': return 'status-info';
            default: return 'status-info';
        }
    };
</script>

<span class="status-badge {getBadgeClass(type)}">
    {text}
</span>

<style>
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }

    .status-safe { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
    .status-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
    .status-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; }
    .status-info { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
</style>
