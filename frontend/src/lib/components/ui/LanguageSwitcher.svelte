<script lang="ts">
    import { locale } from 'svelte-i18n';

    function switchLang(lang: string) {
        $locale = lang;
    }
</script>

<div class="flex gap-2 text-sm font-medium">
    <button 
        class="px-2 py-1 rounded transition-colors {$locale === 'en' ? 'text-blue-400 bg-blue-400/10' : 'text-gray-500 hover:text-gray-300'}"
        onclick={() => switchLang('en')}>
        EN
    </button>
    <span class="text-gray-700">|</span>
    <button 
        class="px-2 py-1 rounded transition-colors {$locale === 'tr' ? 'text-blue-400 bg-blue-400/10' : 'text-gray-500 hover:text-gray-300'}"
        onclick={() => switchLang('tr')}>
        TR
    </button>
</div>