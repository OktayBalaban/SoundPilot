<script lang="ts">
    import { t } from 'svelte-i18n';
    import LanguageSwitcher from './LanguageSwitcher.svelte';

    interface Props {
        isProcessing: boolean;
        onUpload: (e: Event) => void;
    }

    let { isProcessing, onUpload }: Props = $props();
</script>

<header class="max-w-5xl mx-auto mb-10 flex justify-between items-start border-b border-gray-200 pb-8">
    <div>
        <h1 class="text-4xl font-black tracking-tighter text-gray-900">
            {$t('app.title')}
        </h1>
    </div>

    <div class="flex flex-col items-end gap-4">
        <LanguageSwitcher />
        
        <label class="relative group cursor-pointer">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-xl blur opacity-30 group-hover:opacity-75 transition duration-500"></div>
            <div class="relative flex items-center bg-white rounded-xl px-8 py-4 leading-none border border-gray-200 shadow-sm transition-all active:scale-95">
                <span class="text-gray-700 font-bold group-hover:text-blue-600 transition duration-200">
                    {isProcessing ? $t('upload.processing') : $t('upload.button')}
                </span>
            </div>
            <input type="file" accept="audio/*" class="hidden" onchange={onUpload} disabled={isProcessing} />
        </label>
    </div>
</header>