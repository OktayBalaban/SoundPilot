<script lang="ts">
    import type { Track } from '$lib/types';
    
    // Svelte 5 bindable props
    let { 
        track = $bindable(), 
        audioElement = $bindable() 
    } = $props<{ 
        track: Track, 
        audioElement: HTMLAudioElement | null 
    }>();
</script>

<div class="grid grid-cols-[120px_1fr_150px] items-center gap-4 bg-gray-800/40 p-3 rounded-lg border border-gray-700 hover:border-gray-500 transition-all mb-2">
    <div class="flex flex-col gap-2 border-r border-gray-700 pr-4">
        <span class="text-white font-bold uppercase text-[10px] tracking-widest truncate">
            {track.name}
        </span>
        <button 
            class="px-2 py-1 text-[10px] rounded font-bold transition-all
            {track.isMuted ? 'bg-red-500/20 text-red-400 border border-red-500/50' : 'bg-gray-700 text-gray-400 hover:bg-gray-600'}"
            onclick={() => track.isMuted = !track.isMuted}
        >
            {track.isMuted ? 'MUTED' : 'MUTE'}
        </button>
    </div>

    <div class="flex-1 px-4">
        <audio 
            bind:this={audioElement}
            src={track.url}
            muted={track.isMuted}
            bind:volume={track.volume}
            preload="auto"
        ></audio>
        <div class="h-8 bg-gray-900/50 rounded flex items-center px-3">
             <div class="w-full h-1 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500/30" style="width: 100%"></div>
             </div>
        </div>
    </div>

    <div class="flex items-center gap-3 px-2">
        <span class="text-[10px] text-gray-500 font-mono w-6">VOL</span>
        <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.01" 
            bind:value={track.volume}
            class="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
    </div>
</div>