import { apiClient } from '$lib/api/client';
import type { Track, SongEntry } from '$lib/types';

export class ProjectController {
    isProcessing = $state(false);
    tracks = $state<Track[]>([]);
    globalPitch = $state(0);
    error = $state<string | null>(null);
    sessionId = $state(0);

    library = $state<SongEntry[]>([]);
    isLibraryLoading = $state(false);
    currentSongId = $state<string | null>(null);

    private loadTracks(newTracks: Track[], songId: string | null = null) {
        this.tracks = [];
        this.sessionId++;
        this.currentSongId = songId;

        // Let Svelte destroy old mixer before creating new one
        requestAnimationFrame(() => {
            this.tracks = newTracks;
        });
    }

    async handleUpload(file: File | undefined) {
        if (!file) return;

        this.isProcessing = true;
        this.error = null;
        this.tracks = [];
        this.sessionId++;

        try {
            const response = await apiClient.separateAudio(file);
            this.loadTracks(
                this.mapResponseToTracks(response.processed_files),
                response.job_id
            );
            await this.loadLibrary();
        } catch (err) {
            this.error = err instanceof Error ? err.message : 'Unknown error occurred during processing';
        } finally {
            this.isProcessing = false;
        }
    }

    async handleURL(url: string) {
        if (!url.trim()) return;

        this.isProcessing = true;
        this.error = null;
        this.tracks = [];
        this.sessionId++;

        try {
            const response = await apiClient.separateFromURL(url);
            this.loadTracks(
                this.mapResponseToTracks(response.processed_files),
                response.job_id
            );
            await this.loadLibrary();
        } catch (err) {
            this.error = err instanceof Error ? err.message : 'Unknown error occurred during processing';
        } finally {
            this.isProcessing = false;
        }
    }

    async loadLibrary() {
        this.isLibraryLoading = true;
        try {
            const response = await apiClient.getLibrary();
            this.library = response.songs;
        } catch {
            this.library = [];
        } finally {
            this.isLibraryLoading = false;
        }
    }

    loadSong(song: SongEntry) {
        if (!song.is_valid) return;
        if (this.currentSongId === song.id) return;

        this.error = null;

        const newTracks = Object.entries(song.stems).map(([name, url]) => ({
            id: crypto.randomUUID(),
            name: name.charAt(0).toUpperCase() + name.slice(1),
            labelKey: ['vocals', 'drums', 'bass', 'other'].includes(name) ? `tracks.${name}` : undefined,
            url,
            isMuted: false,
            volume: 1.0,
            pitch: 0
        }));

        this.loadTracks(newTracks, song.id);
    }

    async deleteSong(songId: string) {
        try {
            await apiClient.deleteSong(songId);
            this.library = this.library.filter(s => s.id !== songId);
            if (this.currentSongId === songId) {
                this.tracks = [];
                this.sessionId++;
                this.currentSongId = null;
            }
        } catch (err) {
            this.error = err instanceof Error ? err.message : 'Failed to delete song';
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