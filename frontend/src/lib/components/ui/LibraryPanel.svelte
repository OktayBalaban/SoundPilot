<script lang="ts">
    import type { SongEntry } from '$lib/types';

    interface Props {
        songs: SongEntry[];
        isLoading: boolean;
        currentSongId: string | null;
        onSelect: (song: SongEntry) => void;
        onDelete: (songId: string) => void;
        onRefresh: () => void;
    }

    let { songs, isLoading, currentSongId, onSelect, onDelete, onRefresh }: Props = $props();

    function confirmDelete(e: Event, songId: string) {
        e.stopPropagation();
        if (confirm('Delete this song?')) {
            onDelete(songId);
        }
    }
</script>

<div class="playlist">
    <div class="playlist-header">
        <span class="playlist-title">Library</span>
        <div class="playlist-actions">
            <span class="playlist-count">{songs.length} songs</span>
            <button onclick={onRefresh} class="refresh-btn" title="Refresh">↻</button>
        </div>
    </div>

    {#if isLoading}
        <div class="playlist-empty">Loading...</div>
    {:else if songs.length === 0}
        <div class="playlist-empty">No songs yet</div>
    {:else}
        <div class="playlist-items">
            {#each songs as song, i (song.id)}
                <div
                    onclick={() => onSelect(song)}
                    onkeydown={(e) => e.key === 'Enter' && onSelect(song)}
                    role="button"
                    tabindex="0"
                    class="playlist-item {currentSongId === song.id ? 'active' : ''} {!song.is_valid ? 'invalid' : ''}"
                >
                    <span class="item-index">
                        {#if currentSongId === song.id}
                            <span class="now-playing">▶</span>
                        {:else}
                            {i + 1}
                        {/if}
                    </span>

                    <span class="item-title">{song.title}</span>

                    {#if !song.is_valid}
                        <span class="item-badge">!</span>
                    {/if}

                    <button
                        onclick={(e) => confirmDelete(e, song.id)}
                        class="item-delete"
                        title="Delete"
                    >
                        ×
                    </button>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .playlist {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    .playlist-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 18px;
        border-bottom: 1px solid var(--border);
    }

    .playlist-title {
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .playlist-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .playlist-count {
        font-size: 12px;
        color: var(--text-muted);
    }

    .refresh-btn {
        background: none;
        border: none;
        color: var(--text-muted);
        font-size: 14px;
        cursor: pointer;
        padding: 2px 4px;
        border-radius: 4px;
        transition: color 0.15s;
    }

    .refresh-btn:hover {
        color: var(--text-primary);
    }

    .playlist-empty {
        padding: 32px;
        text-align: center;
        font-size: 13px;
        color: var(--text-muted);
    }

    .playlist-items {
        max-height: 300px;
        overflow-y: auto;
    }

    .playlist-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 18px;
        cursor: pointer;
        transition: background 0.1s;
    }

    .playlist-item:hover {
        background: var(--bg-hover);
    }

    .playlist-item.active {
        background: var(--accent-dim);
    }

    .playlist-item.invalid {
        opacity: 0.45;
    }

    .item-index {
        font-family: var(--font-mono);
        font-size: 12px;
        color: var(--text-muted);
        width: 20px;
        text-align: center;
        flex-shrink: 0;
    }

    .now-playing {
        color: var(--accent);
        font-size: 10px;
    }

    .item-title {
        flex: 1;
        font-size: 13px;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .playlist-item.active .item-title {
        color: var(--accent);
    }

    .item-badge {
        font-size: 10px;
        color: var(--danger);
        font-weight: 700;
        flex-shrink: 0;
    }

    .item-delete {
        opacity: 0;
        background: none;
        border: none;
        color: var(--text-muted);
        font-size: 16px;
        cursor: pointer;
        padding: 0 4px;
        flex-shrink: 0;
        transition: all 0.1s;
    }

    .playlist-item:hover .item-delete {
        opacity: 1;
    }

    .item-delete:hover {
        color: var(--danger);
    }
</style>