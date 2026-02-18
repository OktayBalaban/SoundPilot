<script lang="ts">
    import { ProjectController } from '$lib/logic/ProjectController.svelte';
    import AudioMixer from '$lib/components/AudioMixer.svelte';
    import Header from '$lib/components/ui/Header.svelte';
    import ProcessingOverlay from '$lib/components/ui/ProcessingOverlay.svelte';
    import EmptyProjectState from '$lib/components/ui/EmptyProjectState.svelte';
    import ErrorMessage from '$lib/components/ui/ErrorMessage.svelte';

    const project = new ProjectController();

    function onFileSelected(e: Event) {
        const input = e.target as HTMLInputElement;
        project.handleUpload(input.files?.[0]);
    }
</script>

<div class="min-h-screen font-sans p-6">
    <Header 
        isProcessing={project.isProcessing} 
        onUpload={onFileSelected} 
    />

    <main class="max-w-5xl mx-auto">
        {#if project.error}
            <ErrorMessage message={project.error} />
        {/if}

        {#if project.isProcessing}
            <ProcessingOverlay />
        {:else if project.tracks.length > 0}
            <div class="fade-in">
                <AudioMixer bind:tracks={project.tracks} />
            </div>
        {:else}
            <EmptyProjectState />
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