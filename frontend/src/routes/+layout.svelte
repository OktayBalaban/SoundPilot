<script lang="ts">
    import './layout.css';
    import '$lib/i18n';
    import { isLoading, locale } from 'svelte-i18n';
    
    let { children } = $props();

    $effect(() => {
        if ($locale) {
            document.documentElement.setAttribute('lang', $locale);
        }
    });
</script>

{#if $isLoading}
    <div class="min-h-screen bg-gray-950 flex items-center justify-center text-gray-500">
        Loading resources...
    </div>
{:else}
    {@render children()}
{/if}