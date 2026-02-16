import type { ProcessResponse } from '$lib/types';

const API_BASE = 'http://127.0.0.1:8000';

export const apiClient = {
    async separateAudio(file: File): Promise<ProcessResponse> {
        const formData = new FormData();
        formData.append('file', file);

        console.log("Uploading file to:", `${API_BASE}/api/v1/processor/process`);

        try {
            const response = await fetch(`${API_BASE}/api/v1/processor/process`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server Error (${response.status}): ${errorText}`);
            }

            const data: ProcessResponse = await response.json();
            console.log("SERVER RESPONSE (JSON):", data);
            return data;

        } catch (error) {
            console.error("API Error Detail:", error);
            throw error;
        }
    },


    getAudioUrl(filePath: string): string {
        if (!filePath) return '';
        return `${API_BASE}${filePath}`;
    }
};