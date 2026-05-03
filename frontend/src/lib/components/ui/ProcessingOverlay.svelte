<script lang="ts">
    import { t } from 'svelte-i18n';
</script>

<div class="processing">
    <div class="spinner"></div>
    <h2 class="processing-title">{$t('status.separating')}</h2>
    <p class="processing-desc">{$t('status.wait')}</p>
</div>

<style>
    .processing {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 20px;
        text-align: center;
    }

    .spinner {
        width: 32px;
        height: 32px;
        border: 2px solid var(--border);
        border-top-color: var(--accent);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 20px;
    }

    .processing-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 6px;
    }

    .processing-desc {
        font-size: 13px;
        color: var(--text-muted);
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>