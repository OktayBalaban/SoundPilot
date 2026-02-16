<script lang="ts">
    import type { Track } from '$lib/types';

    // Svelte 5 Props (Dışarıdan veri alma yöntemi)
    let { track } = $props<{ track: Track }>();
</script>

<div class="flex items-center gap-4 bg-gray-800 p-4 rounded-lg border border-gray-700 shadow-md mb-3 hover:border-gray-600 transition-colors">
    
    <div class="w-24 flex flex-col gap-2 border-r border-gray-700 pr-4">
        <span class="text-white font-bold uppercase text-xs tracking-widest truncate" title={track.name}>
            {track.name}
        </span>
        
        <button 
            class="px-2 py-1 text-xs rounded font-bold transition-colors duration-200 border border-transparent
            {track.isMuted ? 'bg-red-500/20 text-red-400 border-red-500/50' : 'bg-gray-700 text-gray-400 hover:bg-gray-600'}"
            onclick={() => track.isMuted = !track.isMuted}
        >
            {track.isMuted ? 'MUTED' : 'MUTE'}
        </button>
    </div>

    <div class="flex-1">
        <audio 
            controls 
            class="w-full h-10 block opacity-90 rounded filter invert-[.1]" 
            src={track.url}
            muted={track.isMuted}
        ></audio>
    </div>
</div>