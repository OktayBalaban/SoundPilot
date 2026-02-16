<script lang="ts">
    import { apiClient } from '$lib/api/client';
    import TrackRow from '$lib/components/TrackRow.svelte';
    import type { Track } from '$lib/types';

    // Svelte 5 Runes: State tanımları
    let isProcessing = $state(false);
    let tracks = $state<Track[]>([]);
    let error = $state<string | null>(null);

    async function handleUpload(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;

        const file = input.files[0];
        
        // Reset state
        isProcessing = true;
        error = null;
        tracks = [];

        try {
            const response = await apiClient.separateAudio(file);
            
            // Backend'den gelen yolları Track modeline çevir
            tracks = response.processed_files.map((path, index) => {
                // Dosya adını bul (vocals.wav -> vocals)
                let name = path.split(/[/\\]/).pop()?.replace('.wav', '') || `Track ${index}`;
                // İlk harfi büyüt
                name = name.charAt(0).toUpperCase() + name.slice(1);

                return {
                    id: crypto.randomUUID(),
                    name: name,
                    url: apiClient.getAudioUrl(path),
                    isMuted: false,
                    volume: 1.0
                };
            });
            
        } catch (err) {
            console.error(err);
            error = err instanceof Error ? err.message : 'Unknown error';
        } finally {
            isProcessing = false;
        }
    }
</script>

<div class="min-h-screen bg-gray-900 text-gray-100 font-sans p-6">
    <header class="max-w-4xl mx-auto mb-10 flex justify-between items-center border-b border-gray-800 pb-6">
        <div>
            <h1 class="text-3xl font-bold tracking-tight text-white">
                AISound <span class="text-purple-500">Studio</span>
            </h1>
            <p class="text-gray-500 text-sm mt-1">Clean Architecture Demucs Implementation</p>
        </div>
        
        <label class="relative group cursor-pointer">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg blur opacity-60 group-hover:opacity-100 transition duration-200"></div>
            <div class="relative flex items-center bg-gray-900 rounded-lg px-6 py-3 leading-none border border-gray-800">
                <span class="text-gray-100 font-medium group-hover:text-white transition duration-200">
                    {isProcessing ? 'Processing...' : 'Upload Song'}
                </span>
            </div>
            <input type="file" accept="audio/*" class="hidden" onchange={handleUpload} disabled={isProcessing} />
        </label>
    </header>

    <main class="max-w-4xl mx-auto">
        {#if error}
            <div class="bg-red-900/50 border border-red-500/50 text-red-200 p-4 rounded-lg mb-6 flex items-center gap-3">
                <span class="text-xl">⚠️</span>
                <p>{error}</p>
            </div>
        {/if}

        {#if isProcessing}
            <div class="flex flex-col items-center justify-center py-24 animate-pulse">
                <div class="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                <p class="text-gray-400 font-medium">AI is separating stems... This may take a while.</p>
            </div>
        
        {:else if tracks.length > 0}
            <div class="grid gap-2 fade-in">
                {#each tracks as track (track.id)}
                    <TrackRow {track} />
                {/each}
            </div>
            
        {:else}
            <div class="text-center py-24 border-2 border-dashed border-gray-800 rounded-xl text-gray-600 bg-gray-900/50">
                <div class="text-4xl mb-4 opacity-50">🎵</div>
                <p class="text-lg font-medium">No tracks loaded</p>
                <p class="text-sm">Upload a song to start splitting vocals, drums, and bass.</p>
            </div>
        {/if}
    </main>
</div>

<style>
    /* Basit bir animasyon */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>