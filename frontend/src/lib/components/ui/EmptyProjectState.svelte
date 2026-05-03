<script lang="ts">
    import { t } from 'svelte-i18n';
</script>

<div class="empty">
    <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>
        </svg>
    </div>
    <p class="empty-title">{$t('empty.title')}</p>
    <p class="empty-desc">{$t('empty.description')}</p>
</div>

<style>
    .empty {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 20px;
        border: 1px dashed var(--border);
        border-radius: var(--radius-lg);
        background: var(--bg-secondary);
    }

    .empty-icon {
        color: var(--text-muted);
        margin-bottom: 16px;
        opacity: 0.4;
    }

    .empty-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 6px;
    }

    .empty-desc {
        font-size: 13px;
        color: var(--text-muted);
    }
</style>