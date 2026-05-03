import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/svelte';
// @ts-expect-error: IDE fails to resolve svelte modules in test context
import Header from './Header.svelte';

vi.mock('svelte-i18n', () => ({
    t: { 
        subscribe: (run: (val: any) => void) => {
            run((key: string) => key);
            return () => {};
        } 
    },
    locale: { 
        subscribe: (run: (val: string) => void) => {
            run('en');
            return () => {};
        } 
    }
}));

describe('Header Component', () => {
    it('should disable input and show processing text when isProcessing is true', () => {
        render(Header, {
            isProcessing: true,
            onUpload: vi.fn()
        });

        expect(screen.getByText('upload.processing')).toBeTruthy();
        
        const input = document.querySelector('input[type="file"]') as HTMLInputElement;
        expect(input.disabled).toBe(true);
    });

    it('should trigger onUpload callback when a file is selected', async () => {
        const onUploadMock = vi.fn();
        
        render(Header, {
            isProcessing: false,
            onUpload: onUploadMock
        });

        const input = document.querySelector('input[type="file"]') as HTMLInputElement;
        const file = new File(['(content)'], 'test.mp3', { type: 'audio/mpeg' });

        await fireEvent.change(input, { target: { files: [file] } });

        expect(onUploadMock).toHaveBeenCalled();
    });
});