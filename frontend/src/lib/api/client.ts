import type { ProcessResponse } from '$lib/types';
import { env } from '$env/dynamic/public';

const API_BASE = env.PUBLIC_PROCESSOR_API_BASE_URL || 'http://127.0.0.1:8000';

export const apiClient = {
    async separateAudio(file: File): Promise<ProcessResponse> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/api/v1/processor/process`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error (${response.status}): ${errorText}`);
        }

        return await response.json();
    },

    getAudioUrl(filePath: string): string {
        if (!filePath) return '';

        if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
            return filePath;
        }

        const separator = filePath.startsWith('/') ? '' : '/';
        return `${API_BASE}${separator}${filePath}`;
    }
};