<script lang="ts">
    import { apiClient } from '$lib/api/client';
    import AudioMixer from '$lib/components/AudioMixer.svelte';
    import type { Track } from '$lib/types';

    // Svelte 5 Runes: State tanımları
    let isProcessing = $state(false);
    let tracks = $state<Track[]>([]);
    let error = $state<string | null>(null);

    async function handleUpload(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;

        const file = input.files[0];
        
        // State sıfırlama
        isProcessing = true;
        error = null;
        tracks = [];

        try {
            const response = await apiClient.separateAudio(file);
            
            // Backend'den gelen yolları Track modeline çevir
            tracks = response.processed_files.map((path, index) => {
                let name = path.split(/[/\\]/).pop()?.replace('.wav', '') || `Track ${index}`;
                name = name.charAt(0).toUpperCase() + name.slice(1);

                return {
                    name: name,
                    url: apiClient.getAudioUrl(path),
                    isMuted: false,
                    volume: 1.0
                };
            });
            
        } catch (err) {
            console.error(err);
            error = err instanceof Error ? err.message : 'Bilinmeyen bir hata oluştu';
        } finally {
            isProcessing = false;
        }
    }
</script>

<div class="min-h-screen bg-gray-950 text-gray-100 font-sans p-6">
    <header class="max-w-5xl mx-auto mb-10 flex justify-between items-center border-b border-gray-800 pb-8">
        <div>
            <h1 class="text-4xl font-black tracking-tighter text-white">
                AISound <span class="text-blue-500">Studio</span>
            </h1>
            <p class="text-gray-500 text-sm mt-1 uppercase tracking-widest font-medium">Clean Architecture Demucs Mixer</p>
        </div>
        
        <label class="relative group cursor-pointer">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur opacity-40 group-hover:opacity-100 transition duration-500"></div>
            <div class="relative flex items-center bg-gray-900 rounded-xl px-8 py-4 leading-none border border-gray-800 transition-all active:scale-95">
                <span class="text-gray-100 font-bold group-hover:text-white transition duration-200">
                    {isProcessing ? 'İŞLENİYOR...' : 'ŞARKI YÜKLE'}
                </span>
            </div>
            <input type="file" accept="audio/*" class="hidden" onchange={handleUpload} disabled={isProcessing} />
        </label>
    </header>

    <main class="max-w-5xl mx-auto">
        {#if error}
            <div class="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-xl mb-8 flex items-center gap-4">
                <span class="text-2xl">⚠</span>
                <p class="font-medium">{error}</p>
            </div>
        {/if}

        {#if isProcessing}
            <div class="flex flex-col items-center justify-center py-32 animate-pulse text-center">
                <div class="w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-6"></div>
                <h2 class="text-xl font-bold text-white mb-2">Yapay Zeka Sesleri Ayrıştırıyor</h2>
                <p class="text-gray-500">Bu işlem şarkı uzunluğuna göre 1-2 dakika sürebilir.</p>
            </div>
        
        {:else if tracks.length > 0}
            <div class="fade-in">
                <AudioMixer bind:tracks={tracks} />
            </div>
            
        {:else}
            <div class="text-center py-32 border-2 border-dashed border-gray-800 rounded-3xl text-gray-700 bg-gray-900/20">
                <div class="text-6xl mb-6 grayscale opacity-30">🎹</div>
                <p class="text-xl font-bold text-gray-400">Henüz bir proje yüklenmedi</p>
                <p class="text-gray-600 mt-2">Stem'leri (vokal, davul, bas) ayırmak için bir ses dosyası yükleyin.</p>
            </div>
        {/if}
    </main>
</div>

<style>
    .fade-in {
        animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>