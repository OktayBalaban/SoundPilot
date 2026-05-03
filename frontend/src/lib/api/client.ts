import type { ProcessResponse, LibraryResponse, SongEntry } from '$lib/types';
import { env } from '$env/dynamic/public';

const API_BASE = env.PUBLIC_PROCESSOR_API_BASE_URL || 'http://127.0.0.1:8000';
const STORAGE_BASE = 'http://127.0.0.1:8001';

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

    async separateFromURL(url: string): Promise<ProcessResponse> {
        const response = await fetch(`${API_BASE}/api/v1/processor/process-url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error (${response.status}): ${errorText}`);
        }

        return await response.json();
    },

    async getLibrary(): Promise<LibraryResponse> {
        const response = await fetch(`${STORAGE_BASE}/library`);
        if (!response.ok) throw new Error('Failed to load library');
        return await response.json();
    },

    async getSong(songId: string): Promise<SongEntry> {
        const response = await fetch(`${STORAGE_BASE}/library/${encodeURIComponent(songId)}`);
        if (!response.ok) throw new Error('Song not found');
        return await response.json();
    },

    async deleteSong(songId: string): Promise<void> {
        const response = await fetch(`${STORAGE_BASE}/library/${encodeURIComponent(songId)}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete song');
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