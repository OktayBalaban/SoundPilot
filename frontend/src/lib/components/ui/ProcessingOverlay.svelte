<script lang="ts">
    import { t } from 'svelte-i18n';
</script>

<div class="flex flex-col items-center justify-center py-32 animate-pulse text-center">
    <div class="w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-6"></div>
    <h2 class="text-xl font-bold text-white mb-2">{$t('status.separating')}</h2>
    <p class="text-gray-500">{$t('status.wait')}</p>
</div>