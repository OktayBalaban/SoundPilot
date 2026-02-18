<script lang="ts">
    let { message }: { message: string } = $props();
</script>

<div class="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-xl mb-8 flex items-center gap-4" role="alert">
    <span class="text-2xl">⚠</span>
    <p class="font-medium">{message}</p>
</div>