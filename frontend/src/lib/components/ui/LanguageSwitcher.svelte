<script lang="ts">
    import { locale } from 'svelte-i18n';

    function switchLang(lang: string) {
        $locale = lang;
    }
</script>

<div class="switcher">
    <button
        class="lang-btn {$locale === 'en' ? 'active' : ''}"
        onclick={() => switchLang('en')}>
        EN
    </button>
    <span class="divider">|</span>
    <button
        class="lang-btn {$locale === 'tr' ? 'active' : ''}"
        onclick={() => switchLang('tr')}>
        TR
    </button>
</div>

<style>
    .switcher {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .lang-btn {
        padding: 4px 8px;
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--text-muted);
        background: none;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: color 0.15s;
    }

    .lang-btn:hover {
        color: var(--text-secondary);
    }

    .lang-btn.active {
        color: var(--accent);
    }

    .divider {
        color: var(--text-muted);
        font-size: 12px;
    }
</style>