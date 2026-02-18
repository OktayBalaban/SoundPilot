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

<div class="grid grid-cols-[120px_1fr_100px] sm:grid-cols-[140px_1fr_120px] items-center gap-2 sm:gap-4 bg-black/40 p-3 rounded-lg border border-white/5 hover:border-white/20 transition-all mb-2 overflow-hidden backdrop-blur-sm">
    
    <div class="flex flex-col gap-1 border-r border-white/5 pr-2 sm:pr-4 min-w-0">
        <span class="text-gray-400 font-bold uppercase text-[10px] tracking-[0.12em] truncate" title={track.name}>
            {track.name}
        </span>
        <button 
            class="px-2 py-1 text-[9px] rounded font-black transition-all uppercase
            {track.isMuted ? 'bg-red-950/40 text-red-500 border border-red-900/30' : 'bg-white/5 text-gray-500 hover:bg-white/10'}"
            onclick={() => track.isMuted = !track.isMuted}
        >
            {track.isMuted ? 'MUTED' : 'MUTE'}
        </button>
    </div>

    <div class="min-w-0 px-1 sm:px-2">
        <audio 
            bind:this={audioElement}
            src={track.url}
            muted={track.isMuted}
            bind:volume={track.volume}
            preload="auto"
            crossorigin="anonymous" 
        ></audio>
        
        <div class="h-10 bg-black/60 rounded flex items-center px-4 border border-white/5 shadow-inner">
             <div class="w-full h-[1px] bg-white/10 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500/50 shadow-[0_0_8px_rgba(59,130,246,0.5)]" style="width: 100%"></div>
             </div>
        </div>
    </div>

    <div class="flex items-center gap-2 sm:gap-3 group pl-2 sm:pl-4 border-l border-white/5 min-w-0">
        <span class="text-[9px] text-gray-600 font-bold font-mono w-6 sm:w-7 flex-shrink-0 group-hover:text-gray-400">VOL</span>
        <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.01" 
            bind:value={track.volume}
            class="w-full min-w-0 h-[2px] bg-white/10 rounded-lg appearance-none cursor-pointer accent-blue-600"
        />
    </div>
</div>

<style>
    /* Slider Başlığı (Thumb) */
    input[type="range"]::-webkit-slider-thumb {
        appearance: none;
        height: 10px;
        width: 10px;
        border-radius: 50%;
        background: white;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.5);
    }

    /* Track (Ray) genişliğini zorla */
    input[type="range"] {
        width: 100%;
        background: transparent;
    }
</style>