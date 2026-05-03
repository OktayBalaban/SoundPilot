<script lang="ts">
    import { t } from 'svelte-i18n';
    import LanguageSwitcher from './LanguageSwitcher.svelte';

    interface Props {
        isProcessing: boolean;
        onUpload: (e: Event) => void;
        onURLSubmit: (url: string) => void;
    }

    let { isProcessing, onUpload, onURLSubmit }: Props = $props();
    let urlInput = $state('');

    function handleURLSubmit() {
        if (!urlInput.trim() || isProcessing) return;
        onURLSubmit(urlInput.trim());
        urlInput = '';
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Enter') handleURLSubmit();
    }
</script>

<header class="header">
    <div class="header-top">
        <div class="brand">
            <span class="brand-icon">◆</span>
            <h1 class="brand-name">SoundPilot</h1>
        </div>

        <div class="header-actions">
            <LanguageSwitcher />

            <label class="upload-btn" class:disabled={isProcessing}>
                <span>{isProcessing ? $t('upload.processing') : $t('upload.button')}</span>
                <input type="file" accept="audio/*" onchange={onUpload} disabled={isProcessing} />
            </label>
        </div>
    </div>

    <div class="url-bar">
        <div class="url-input-wrapper">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="url-icon">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
            </svg>
            <input
                type="text"
                bind:value={urlInput}
                onkeydown={handleKeydown}
                placeholder="Paste a YouTube URL..."
                disabled={isProcessing}
                class="url-input"
            />
        </div>
        <button
            onclick={handleURLSubmit}
            disabled={isProcessing || !urlInput.trim()}
            class="url-submit"
        >
            Process
        </button>
    </div>
</header>

<style>
    .header {
        max-width: 1200px;
        margin: 0 auto 32px;
        padding-bottom: 24px;
        border-bottom: 1px solid var(--border);
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-icon {
        color: var(--accent);
        font-size: 20px;
    }

    .brand-name {
        font-family: var(--font-mono);
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
    }

    .header-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .upload-btn {
        display: inline-flex;
        align-items: center;
        padding: 8px 20px;
        background: var(--accent);
        color: #000;
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all 0.15s;
    }

    .upload-btn:hover {
        background: var(--accent-hover);
    }

    .upload-btn.disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .upload-btn input {
        display: none;
    }

    .url-bar {
        display: flex;
        gap: 8px;
    }

    .url-input-wrapper {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 0 14px;
        transition: border-color 0.15s;
    }

    .url-input-wrapper:focus-within {
        border-color: var(--accent);
    }

    .url-icon {
        color: var(--text-muted);
        flex-shrink: 0;
    }

    .url-input {
        flex: 1;
        background: none;
        border: none;
        outline: none;
        color: var(--text-primary);
        font-family: var(--font-body);
        font-size: 14px;
        padding: 12px 0;
    }

    .url-input::placeholder {
        color: var(--text-muted);
    }

    .url-input:disabled {
        opacity: 0.4;
    }

    .url-submit {
        padding: 12px 24px;
        background: var(--bg-elevated);
        color: var(--text-primary);
        font-family: var(--font-mono);
        font-size: 13px;
        font-weight: 600;
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all 0.15s;
    }

    .url-submit:hover:not(:disabled) {
        background: var(--bg-hover);
        border-color: var(--border-hover);
    }

    .url-submit:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }
</style>