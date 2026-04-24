<script lang="ts">
    import "../app.css";
    const { children } = $props();
</script>

<nav class="glass-nav">
    <div class="nav-content">
        <a href="/" class="logo">
            <span class="otuoke">OTUOKE</span>
            <span class="flood">FloodWatch</span>
        </a>
        <div class="links">
            <a href="/">Dashboard</a>
            <a href="/history">History</a>
            <a href="/alerts">Alerts</a>
        </div>
    </div>
</nav>

<main>
    {@render children()}
</main>

<style>
    .glass-nav {
        position: sticky;
        top: 0;
        z-index: 50;
        background: var(--bg-nav);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 1.5rem;
    }

    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo {
        font-weight: 800;
        font-size: 1.25rem;
        letter-spacing: -0.025em;
        display: flex;
        gap: 0.25rem;
    }

    .otuoke { color: var(--color-safe); }
    .flood { color: var(--text-primary); }

    .links {
        display: flex;
        gap: 2rem;
    }

    .links a {
        color: var(--text-secondary);
        font-weight: 500;
        transition: color 0.2s;
    }

    .links a:hover {
        color: var(--text-primary);
    }

    main {
        max-width: 1200px;
        margin: 0 auto;
        padding-top: 1rem;
    }
</style>
