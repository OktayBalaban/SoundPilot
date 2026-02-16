import type { ProcessResponse } from '$lib/types';

// API Adresi
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

            // ÖNCE HAM VERİYİ ALALIM (DEBUG)
            const responseText = await response.text();
            console.log("RAW SERVER RESPONSE:", responseText); // <-- Tarayıcı konsolunda buna bakacağız!

            if (!response.ok) {
                throw new Error(`Server Error (${response.status}): ${responseText}`);
            }

            // Eğer yanıt boşsa hata fırlat
            if (!responseText) {
                throw new Error("Server returned empty response!");
            }

            // JSON Çevirme Denemesi
            try {
                return JSON.parse(responseText);
            } catch (e) {
                throw new Error(`Invalid JSON format. Server sent: ${responseText.substring(0, 50)}...`);
            }

        } catch (error) {
            console.error("API Error Detail:", error);
            throw error;
        }
    },

    getAudioUrl(filePath: string): string {
        const fileName = filePath.split(/[/\\]/).pop();
        return `${API_BASE}/static/${fileName}`;
    }
};