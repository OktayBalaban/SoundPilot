<script lang="ts">
    import { projectController } from '$lib/logic/ProjectController.svelte';
    import { onMount } from 'svelte';
    import AudioMixer from '$lib/components/AudioMixer.svelte';
    import Header from '$lib/components/ui/Header.svelte';
    import ProcessingOverlay from '$lib/components/ui/ProcessingOverlay.svelte';
    import EmptyProjectState from '$lib/components/ui/EmptyProjectState.svelte';
    import ErrorMessage from '$lib/components/ui/ErrorMessage.svelte';
    import LibraryPanel from '$lib/components/ui/LibraryPanel.svelte';

    function onFileSelected(e: Event) {
        const input = e.target as HTMLInputElement;
        projectController.handleUpload(input.files?.[0]);
    }

    function onURLSubmit(url: string) {
        projectController.handleURL(url);
    }

    onMount(() => {
        projectController.loadLibrary();
    });
</script>

<div class="app">
    <Header
        isProcessing={projectController.isProcessing}
        onUpload={onFileSelected}
        onURLSubmit={onURLSubmit}
    />

    <main class="main">
        {#if projectController.error}
            <ErrorMessage message={projectController.error} />
        {/if}

        {#if projectController.isProcessing}
            <ProcessingOverlay />
        {:else if projectController.tracks.length > 0}
            {#key projectController.sessionId}
                <div class="fade-in">
                    <AudioMixer bind:tracks={projectController.tracks} />
                </div>
            {/key}
        {:else}
            <EmptyProjectState />
        {/if}

        {#if projectController.library.length > 0 || projectController.isLibraryLoading}
            <div class="library-section">
                <LibraryPanel
                    songs={projectController.library}
                    isLoading={projectController.isLibraryLoading}
                    currentSongId={projectController.currentSongId}
                    onSelect={(song) => projectController.loadSong(song)}
                    onDelete={(id) => projectController.deleteSong(id)}
                    onRefresh={() => projectController.loadLibrary()}
                />
            </div>
        {/if}
    </main>
</div>

<style>
    .app {
        min-height: 100vh;
        padding: 24px 32px;
    }

    .main {
        max-width: 900px;
        margin: 0 auto;
    }

    .library-section {
        margin-top: 24px;
    }

    .fade-in {
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>