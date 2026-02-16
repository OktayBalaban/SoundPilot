<script lang="ts">
    import TrackRow from './TrackRow.svelte';
    import type { Track } from '$lib/types';

    let { tracks = $bindable<Track[]>([]) } = $props();

    let isPlaying = $state(false);
    let currentTime = $state(0);
    let duration = $state(0);
    let audioElements = $state<HTMLAudioElement[]>([]);

    function togglePlay() {
        if (tracks.length === 0) return;
        isPlaying = !isPlaying;
        
        audioElements.forEach(audio => {
            if (audio) isPlaying ? audio.play() : audio.pause();
        });
    }

    function handleSeek(e: Event) {
        const targetTime = parseFloat((e.target as HTMLInputElement).value);
        currentTime = targetTime;
        audioElements.forEach(audio => {
            if (audio) audio.currentTime = targetTime;
        });
    }

    $effect(() => {
        let interval: number;
        if (isPlaying) {
            interval = window.setInterval(() => {
                const master = audioElements.find(a => a !== null);
                if (master) {
                    currentTime = master.currentTime;
                    if (duration === 0) duration = master.duration;
                    if (master.ended) {
                        isPlaying = false;
                        currentTime = 0;
                        audioElements.forEach(a => a && (a.currentTime = 0));
                    }
                }
            }, 100);
        }
        return () => clearInterval(interval);
    });
</script>

<div class="bg-gray-900 rounded-3xl border border-gray-800 shadow-2xl overflow-hidden">
    <div class="p-8 bg-gradient-to-b from-gray-800/40 to-transparent border-b border-gray-800">
        <div class="flex items-center gap-8">
            <button 
                onclick={togglePlay}
                class="w-20 h-20 rounded-full bg-blue-600 hover:bg-blue-500 flex items-center justify-center transition-all shadow-xl shadow-blue-900/20 active:scale-90"
            >
                {#if isPlaying}
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-white" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-white translate-x-1" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                {/if}
            </button>

            <div class="flex-1">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <span class="text-xs font-black uppercase tracking-[0.2em] text-blue-500">Master Output</span>
                        <h2 class="text-2xl font-bold text-white">Multitrack Mixer</h2>
                    </div>
                    <div class="text-right font-mono text-sm text-gray-400">
                        <span class="text-blue-400">{Math.floor(currentTime)}s</span> / {Math.floor(duration || 0)}s
                    </div>
                </div>
                <input 
                    type="range" 
                    min="0" 
                    max={duration || 100} 
                    step="0.1"
                    value={currentTime} 
                    oninput={handleSeek}
                    class="w-full h-3 bg-gray-800 rounded-full appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400 transition-all"
                />
            </div>
        </div>
    </div>

    <div class="p-6 space-y-3">
        {#each tracks as track, i}
            <TrackRow bind:track={tracks[i]} bind:audioElement={audioElements[i]} />
        {/each}
    </div>
</div>