<script lang="ts">
    import { t } from 'svelte-i18n';
    import LanguageSwitcher from './LanguageSwitcher.svelte';

    interface Props {
        isProcessing: boolean;
        onUpload: (e: Event) => void;
    }

    let { isProcessing, onUpload }: Props = $props();
</script>

<header class="max-w-5xl mx-auto mb-10 flex justify-between items-start border-b border-gray-800 pb-8">
    <div>
        <h1 class="text-4xl font-black tracking-tighter text-white">
            {$t('app.title')} <span class="text-blue-500">{$t('app.subtitle')}</span>
        </h1>
        <p class="text-gray-500 text-sm mt-1 uppercase tracking-widest font-medium">
            {$t('app.description')}
        </p>
    </div>

    <div class="flex flex-col items-end gap-4">
        <LanguageSwitcher />
        
        <label class="relative group cursor-pointer">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur opacity-40 group-hover:opacity-100 transition duration-500"></div>
            <div class="relative flex items-center bg-gray-900 rounded-xl px-8 py-4 leading-none border border-gray-800 transition-all active:scale-95">
                <span class="text-gray-100 font-bold group-hover:text-white transition duration-200">
                    {isProcessing ? $t('upload.processing') : $t('upload.button')}
                </span>
            </div>
            <input type="file" accept="audio/*" class="hidden" onchange={onUpload} disabled={isProcessing} />
        </label>
    </div>
</header>