<script lang="ts">
    import TrackRow from './TrackRow.svelte';
    import type { Track } from '$lib/types';
    import { projectController } from '$lib/logic/ProjectController.svelte';
    import { onMount } from 'svelte';

    let { tracks = $bindable<Track[]>([]) } = $props();

    let isPlaying = $state(false);
    let currentTime = $state(0);
    let duration = $state(0);
    let audioElements = $state<HTMLAudioElement[]>([]);

    function stopAll() {
        isPlaying = false;
        currentTime = 0;
        duration = 0;
        audioElements.forEach(a => {
            if (a) {
                a.pause();
                a.currentTime = 0;
            }
        });
    }

    function togglePlay() {
        if (tracks.length === 0) return;
        isPlaying = !isPlaying;

        audioElements.forEach(audio => {
            if (audio) {
                isPlaying ? audio.play() : audio.pause();
            }
        });
    }

    function handleSeek(e: Event) {
        const targetTime = parseFloat((e.target as HTMLInputElement).value);
        currentTime = targetTime;
        audioElements.forEach(audio => {
            if (audio) audio.currentTime = targetTime;
        });
    }

    function formatTime(seconds: number): string {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    onMount(() => {
        return () => {
            // Cleanup on destroy — stop all audio
            audioElements.forEach(a => {
                if (a) {
                    a.pause();
                    a.src = '';
                }
            });
        };
    });

    $effect(() => {
        let interval: number;
        if (isPlaying) {
            interval = window.setInterval(() => {
                const master = audioElements.find(a => a && a.readyState >= 2);
                if (master) {
                    currentTime = master.currentTime;
                    if (duration === 0) duration = master.duration;
                    if (master.ended) {
                        stopAll();
                    }
                }
            }, 100);
        }
        return () => clearInterval(interval);
    });
</script>

<div class="mixer">
    <div class="transport">
        <button onclick={togglePlay} class="play-btn">
            {#if isPlaying}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
            {:else}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            {/if}
        </button>

        <div class="time-display">
            <span class="time-current">{formatTime(currentTime)}</span>
            <span class="time-sep">/</span>
            <span class="time-total">{formatTime(duration || 0)}</span>
        </div>

        <div class="pitch-control">
            <span class="pitch-label">PITCH</span>
            <button onclick={() => projectController.setGlobalPitch(projectController.globalPitch - 1)} class="pitch-btn">−</button>
            <span class="pitch-value" class:positive={projectController.globalPitch > 0} class:negative={projectController.globalPitch < 0}>
                {projectController.globalPitch > 0 ? '+' : ''}{projectController.globalPitch}
            </span>
            <button onclick={() => projectController.setGlobalPitch(projectController.globalPitch + 1)} class="pitch-btn">+</button>
        </div>

        <div class="seek-bar">
            <input
                type="range"
                min="0"
                max={duration || 100}
                step="0.1"
                value={currentTime}
                oninput={handleSeek}
                class="seek-input"
            />
            <div class="seek-progress" style="width: {duration ? (currentTime / duration) * 100 : 0}%"></div>
        </div>
    </div>

    <div class="tracks">
        {#each tracks as track, i (track.id)}
            <TrackRow bind:track={tracks[i]} bind:audioElement={audioElements[i]} />
        {/each}
    </div>
</div>

<style>
    .mixer {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    .transport {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 20px;
        border-bottom: 1px solid var(--border);
        flex-wrap: wrap;
    }

    .play-btn {
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--accent);
        color: #fff;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.15s;
        flex-shrink: 0;
    }

    .play-btn:hover {
        background: var(--accent-hover);
        transform: scale(1.05);
    }

    .time-display {
        font-family: var(--font-mono);
        font-size: 13px;
        color: var(--text-secondary);
        flex-shrink: 0;
    }

    .time-current { color: var(--text-primary); }
    .time-sep { color: var(--text-muted); margin: 0 2px; }
    .time-total { color: var(--text-muted); }

    .pitch-control {
        display: flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-primary);
        padding: 6px 12px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
        flex-shrink: 0;
    }

    .pitch-label {
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 600;
        color: var(--text-muted);
        letter-spacing: 0.1em;
        margin-right: 4px;
    }

    .pitch-btn {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-elevated);
        color: var(--text-secondary);
        border: 1px solid var(--border);
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.1s;
    }

    .pitch-btn:hover {
        background: var(--bg-hover);
        color: var(--text-primary);
    }

    .pitch-value {
        font-family: var(--font-mono);
        font-size: 14px;
        font-weight: 600;
        width: 28px;
        text-align: center;
        color: var(--text-primary);
    }

    .pitch-value.positive { color: var(--accent); }
    .pitch-value.negative { color: var(--danger); }

    .seek-bar {
        flex: 1;
        min-width: 200px;
        position: relative;
        height: 4px;
        background: var(--bg-primary);
        border-radius: 2px;
        align-self: center;
    }

    .seek-progress {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: var(--accent);
        border-radius: 2px;
        pointer-events: none;
    }

    .seek-input {
        position: absolute;
        top: -8px;
        left: 0;
        width: 100%;
        height: 20px;
        opacity: 0;
        cursor: pointer;
    }

    .tracks {
        padding: 8px;
    }
</style>