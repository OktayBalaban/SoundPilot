import { apiClient } from '$lib/api/client';
import type { Track } from '$lib/types';

export class ProjectController {
    isProcessing = $state(false);
    tracks = $state<Track[]>([]);
    error = $state<string | null>(null);

    async handleUpload(file: File | undefined) {
        if (!file) return;

        this.isProcessing = true;
        this.error = null;
        this.tracks = [];

        try {
            const response = await apiClient.separateAudio(file);
            this.tracks = this.mapResponseToTracks(response.processed_files);
        } catch (err) {
            this.error = err instanceof Error ? err.message : 'Unknown error occurred during processing';
        } finally {
            this.isProcessing = false;
        }
    }

    private mapResponseToTracks(filePaths: string[]): Track[] {
        return filePaths.map((path, index) => {
            const rawName = path.split(/[/\\]/).pop()?.replace('.wav', '') || `Track ${index}`;
            // Eğer isim standart bir enstrüman ise key ata
            const key = ['vocals', 'drums', 'bass', 'other'].includes(rawName.toLowerCase()) 
                ? `tracks.${rawName.toLowerCase()}` 
                : undefined;
            
            const formattedName = rawName.charAt(0).toUpperCase() + rawName.slice(1);

            return {
                id: crypto.randomUUID(),
                name: formattedName,
                labelKey: key, // Yeni alan
                url: apiClient.getAudioUrl(path),
                isMuted: false,
                volume: 1.0
            };
        });
    }
}