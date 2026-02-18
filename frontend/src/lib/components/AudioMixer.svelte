<script lang="ts">
    import TrackRow from './TrackRow.svelte';
    import type { Track } from '$lib/types';
    import { projectController } from '$lib/logic/ProjectController.svelte';

    let { tracks = $bindable<Track[]>([]) } = $props();

    let isPlaying = $state(false);
    let currentTime = $state(0);
    let duration = $state(0);
    let audioElements = $state<HTMLAudioElement[]>([]);

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

    // Senkronizasyon ve Bitiş Kontrolü
    $effect(() => {
        let interval: number;
        if (isPlaying) {
            interval = window.setInterval(() => {
                // Referans olarak çalmaya hazır ilk elementi seç
                const master = audioElements.find(a => a && a.readyState >= 2);
                
                if (master) {
                    currentTime = master.currentTime;
                    if (duration === 0) duration = master.duration;

                    // --- KRİTİK HATA ÇÖZÜMÜ ---
                    if (master.ended) {
                        isPlaying = false;
                        currentTime = 0;
                        
                        // Sadece başa sarma, hepsini tek tek DURDUR (Explicit Pause)
                        audioElements.forEach(a => {
                            if (a) {
                                a.pause();
                                a.currentTime = 0;
                            }
                        });
                    }
                }
            }, 100);
        }
        return () => clearInterval(interval);
    });
</script>

<div class="bg-[#0a0a0a] rounded-3xl border border-white/5 shadow-2xl overflow-hidden">
    <div class="p-8 bg-gradient-to-b from-white/[0.03] to-transparent border-b border-white/5">
        <div class="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
            
            <button 
                onclick={togglePlay}
                class="w-20 h-20 flex-shrink-0 rounded-full bg-blue-600 hover:bg-blue-500 flex items-center justify-center transition-all shadow-xl shadow-blue-900/40 active:scale-95"
            >
                {#if isPlaying}
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-white" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 fill-white translate-x-1" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                {/if}
            </button>

            <div class="flex flex-wrap items-center gap-4">
                <div class="flex items-center gap-4 bg-black/40 px-5 py-2.5 rounded-2xl border border-white/5">
                    <span class="text-[9px] font-black tracking-widest text-gray-500 uppercase">Pitch</span>
                    <div class="flex items-center gap-2">
                        <button onclick={() => projectController.setGlobalPitch(projectController.globalPitch - 1)} class="w-7 h-7 rounded-lg border border-white/10 hover:bg-white/5 text-white">-</button>
                        <div class="w-10 text-center">
                            <span class="text-lg font-black font-mono text-emerald-500">{projectController.globalPitch > 0 ? '+' : ''}{projectController.globalPitch}</span>
                        </div>
                        <button onclick={() => projectController.setGlobalPitch(projectController.globalPitch + 1)} class="w-7 h-7 rounded-lg border border-white/10 hover:bg-white/5 text-white">+</button>
                    </div>
                </div>
            </div>

            <div class="flex-1 w-full">
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
                    class="w-full h-2 bg-white/5 rounded-full appearance-none cursor-pointer accent-blue-500"
                />
            </div>
        </div>
    </div>

    <div class="p-6 space-y-2">
        {#each tracks as track, i (track.id)}
            <TrackRow bind:track={tracks[i]} bind:audioElement={audioElements[i]} />
        {/each}
    </div>
</div>