import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer';

export default defineConfig({
    plugins: [sveltekit()],
    css: {
        postcss: {
            plugins: [
                tailwindcss(), 
                autoprefixer()
            ],
        },
    },
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}'],
        environment: 'jsdom',
        globals: true,
        setupFiles: ['./src/vitest.setup.ts']
    },
    resolve: {
        conditions: process.env.VITEST ? ['browser'] : undefined
    }
});