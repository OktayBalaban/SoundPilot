<script lang="ts">
    import { t } from 'svelte-i18n';
</script>

<div class="text-center py-32 border-2 border-dashed border-gray-800 rounded-3xl text-gray-700 bg-gray-900/20">
    <div class="text-6xl mb-6 grayscale opacity-30">🎹</div>
    <p class="text-xl font-bold text-gray-400">{$t('empty.title')}</p>
    <p class="text-gray-600 mt-2">{$t('empty.description')}</p>
</div>