<script lang="ts">
    import type { Track } from '$lib/types';
    import { projectController } from '$lib/logic/ProjectController.svelte';
    import { onMount } from 'svelte';
    import * as Tone from 'tone';

    let {
        track = $bindable(),
        audioElement = $bindable()
    } = $props<{
        track: Track,
        audioElement: HTMLAudioElement | null
    }>();

    let pitchShift: Tone.PitchShift | null = null;
    let isInitialized = $state(false);

    const trackColors: Record<string, string> = {
        vocals: '#e8922a',
        drums: '#e05555',
        bass: '#4caf6a',
        other: '#5a9fd4'
    };

    function getTrackColor(): string {
        const key = track.name.toLowerCase();
        return trackColors[key] || '#9fb3b3';
    }

    onMount(() => {
        if (audioElement) {
            pitchShift = new Tone.PitchShift(projectController.globalPitch);
            const source = Tone.getContext().createMediaElementSource(audioElement);
            Tone.connect(source, pitchShift);
            pitchShift.toDestination();
            isInitialized = true;
        }
        return () => { pitchShift?.dispose(); };
    });

    $effect(() => {
        if (pitchShift && isInitialized) {
            pitchShift.pitch = projectController.globalPitch;
            if (Tone.getContext().state !== 'running') Tone.start();
        }
    });
</script>

<div class="track" class:muted={track.isMuted}>
    <div class="track-color" style="background: {getTrackColor()}"></div>

    <div class="track-name">
        <span class="name-text">{track.name}</span>
    </div>

    <button
        class="mute-btn" class:active={track.isMuted}
        onclick={() => track.isMuted = !track.isMuted}
    >
        M
    </button>

    <div class="track-spacer">
        <audio
            bind:this={audioElement}
            src={track.url}
            muted={track.isMuted}
            bind:volume={track.volume}
            preload="auto"
            crossorigin="anonymous"
        ></audio>
    </div>

    <div class="volume-control">
        <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            bind:value={track.volume}
            class="volume-slider"
        />
        <span class="volume-value">{Math.round(track.volume * 100)}</span>
    </div>
</div>

<style>
    .track {
        display: grid;
        grid-template-columns: 3px 100px 32px 1fr 140px;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        background: var(--bg-primary);
        border-radius: var(--radius-sm);
        margin-bottom: 4px;
        transition: opacity 0.15s;
    }

    .track:hover {
        background: var(--bg-elevated);
    }

    .track.muted {
        opacity: 0.4;
    }

    .track-color {
        width: 3px;
        height: 28px;
        border-radius: 2px;
    }

    .track-name {
        min-width: 0;
    }

    .name-text {
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--text-primary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .mute-btn {
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
        background: var(--bg-elevated);
        color: var(--text-muted);
        border: 1px solid var(--border);
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.1s;
    }

    .mute-btn:hover {
        border-color: var(--border-hover);
    }

    .mute-btn.active {
        background: rgba(224, 85, 85, 0.15);
        color: var(--danger);
        border-color: rgba(224, 85, 85, 0.3);
    }

    .track-spacer {
        min-height: 32px;
    }

    .volume-control {
        display: flex;
        align-items: center;
        gap: 6px;
        padding-right: 4px;
    }

    .volume-slider {
        flex: 1;
        height: 4px;
        -webkit-appearance: none;
        appearance: none;
        background: var(--bg-hover);
        border-radius: 2px;
        outline: none;
        cursor: pointer;
        min-width: 0;
    }

    .volume-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 12px;
        height: 12px;
        background: var(--text-primary);
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }

    .volume-slider::-moz-range-thumb {
        width: 12px;
        height: 12px;
        background: var(--text-primary);
        border-radius: 50%;
        cursor: pointer;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }

    .volume-value {
        font-family: var(--font-mono);
        font-size: 10px;
        color: var(--text-muted);
        width: 22px;
        text-align: right;
        flex-shrink: 0;
    }
</style>