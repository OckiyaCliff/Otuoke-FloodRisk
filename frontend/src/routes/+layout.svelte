<script lang="ts">
    import "../app.css";
    const { children } = $props();

    let mobileMenuOpen = $state(false);

    function toggleMenu() {
        mobileMenuOpen = !mobileMenuOpen;
    }

    function closeMenu() {
        mobileMenuOpen = false;
    }
</script>

<svelte:head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Otuoke FloodWatch — Real-time flood early-warning system for Federal University Otuoke, Bayelsa State. Powered by ML predictions." />
    <title>Otuoke FloodWatch</title>
</svelte:head>

<nav class="top-nav">
    <div class="nav-content">
        <a href="/" class="logo" onclick={closeMenu}>
            <span class="logo-icon">🌊</span>
            <span class="logo-text">
                <span class="otuoke">OTUOKE</span>
                <span class="flood">FloodWatch</span>
            </span>
        </a>

        <!-- Desktop Nav -->
        <div class="nav-links desktop-only">
            <a href="/">Dashboard</a>
            <a href="/history">History</a>
            <a href="/alerts">Alerts</a>
        </div>

        <!-- Hamburger Button -->
        <button class="hamburger mobile-only" onclick={toggleMenu} aria-label="Toggle menu">
            <span class="bar" class:open={mobileMenuOpen}></span>
            <span class="bar" class:open={mobileMenuOpen}></span>
            <span class="bar" class:open={mobileMenuOpen}></span>
        </button>
    </div>

    <!-- Mobile Dropdown -->
    {#if mobileMenuOpen}
        <div class="mobile-dropdown">
            <a href="/" onclick={closeMenu}>🏠 Dashboard</a>
            <a href="/history" onclick={closeMenu}>📊 History</a>
            <a href="/alerts" onclick={closeMenu}>🔔 Alerts</a>
        </div>
    {/if}
</nav>

<main>
    {@render children()}
</main>

<!-- Mobile Bottom Nav -->
<nav class="bottom-nav mobile-only">
    <a href="/" class="bottom-link">
        <span class="bottom-icon">📡</span>
        <span>Live</span>
    </a>
    <a href="/history" class="bottom-link">
        <span class="bottom-icon">📊</span>
        <span>History</span>
    </a>
    <a href="/alerts" class="bottom-link">
        <span class="bottom-icon">🔔</span>
        <span>Alerts</span>
    </a>
</nav>

<style>
    .top-nav {
        position: sticky;
        top: 0;
        z-index: 50;
        background: var(--bg-nav);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid var(--border-color);
        padding: 0.875rem clamp(1rem, 4vw, 1.5rem);
    }

    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .logo-icon {
        font-size: 1.5rem;
    }

    .logo-text {
        font-weight: 800;
        font-size: 1.125rem;
        letter-spacing: -0.025em;
        display: flex;
        gap: 0.25rem;
    }

    .otuoke { color: var(--color-safe); }
    .flood { color: var(--text-primary); }

    .nav-links {
        display: flex;
        gap: 2rem;
    }

    .nav-links a {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.9375rem;
        transition: color 0.2s;
        padding: 0.25rem 0;
    }

    .nav-links a:hover {
        color: var(--text-primary);
    }

    /* Hamburger */
    .hamburger {
        display: flex;
        flex-direction: column;
        gap: 5px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 8px;
        min-width: 44px;
        min-height: 44px;
        align-items: center;
        justify-content: center;
    }

    .bar {
        width: 22px;
        height: 2px;
        background: var(--text-primary);
        border-radius: 2px;
        transition: transform 0.3s, opacity 0.3s;
    }

    .bar.open:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .bar.open:nth-child(2) { opacity: 0; }
    .bar.open:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

    /* Mobile dropdown */
    .mobile-dropdown {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        padding: 0.75rem 0 0.5rem;
        border-top: 1px solid var(--border-color);
        margin-top: 0.75rem;
    }

    .mobile-dropdown a {
        padding: 0.75rem 0.5rem;
        color: var(--text-secondary);
        font-weight: 500;
        border-radius: var(--radius-sm);
        transition: background 0.2s, color 0.2s;
    }

    .mobile-dropdown a:hover {
        background: var(--accent-blue-bg);
        color: var(--text-primary);
    }

    /* Bottom nav */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 50;
        background: var(--bg-nav);
        backdrop-filter: blur(16px);
        border-top: 1px solid var(--border-color);
        display: flex;
        justify-content: space-around;
        padding: 0.5rem 0 calc(0.5rem + env(safe-area-inset-bottom));
    }

    .bottom-link {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.125rem;
        color: var(--text-muted);
        font-size: 0.6875rem;
        font-weight: 500;
        padding: 0.375rem 1rem;
        min-width: 64px;
        min-height: 44px;
        justify-content: center;
        transition: color 0.2s;
    }

    .bottom-link:hover {
        color: var(--accent-blue);
    }

    .bottom-icon {
        font-size: 1.25rem;
    }

    main {
        max-width: 1200px;
        margin: 0 auto;
        padding: clamp(0.75rem, 3vw, 1.5rem);
        padding-bottom: 5rem; /* Space for bottom nav on mobile */
    }

    /* Responsive visibility */
    .desktop-only { display: flex; }
    .mobile-only { display: none; }

    @media (max-width: 768px) {
        .desktop-only { display: none; }
        .mobile-only { display: flex; }

        main {
            padding-bottom: 6rem;
        }
    }
</style>
