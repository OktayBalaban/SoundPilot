import { apiClient } from '$lib/api/client';
import type { Track } from '$lib/types';

export class ProjectController {
    isProcessing = $state(false);
    tracks = $state<Track[]>([]);
    globalPitch = $state(0);
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

    setGlobalPitch(n_steps: number) {
        this.globalPitch = Math.max(-12, Math.min(12, n_steps));
    }

    private mapResponseToTracks(filePaths: string[]): Track[] {
        return filePaths.map((path, index) => {
            const rawName = path.split(/[/\\]/).pop()?.replace('.wav', '') || `Track ${index}`;
            const key = ['vocals', 'drums', 'bass', 'other'].includes(rawName.toLowerCase()) 
                ? `tracks.${rawName.toLowerCase()}` 
                : undefined;
            
            const formattedName = rawName.charAt(0).toUpperCase() + rawName.slice(1);

            return {
                id: crypto.randomUUID(),
                name: formattedName,
                labelKey: key,
                url: apiClient.getAudioUrl(path),
                isMuted: false,
                volume: 1.0,
                pitch: 0
            };
        });
    }
}

export const projectController = new ProjectController();