<script lang="ts">
    let { message }: { message: string } = $props();
</script>

<div class="error" role="alert">
    <span class="error-icon">!</span>
    <p class="error-text">{message}</p>
</div>

<style>
    .error {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: var(--radius-md);
        margin-bottom: 20px;
    }

    .error-icon {
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--danger);
        color: #fff;
        font-size: 11px;
        font-weight: 700;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .error-text {
        font-size: 13px;
        color: #fca5a5;
    }
</style>