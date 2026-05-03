import { apiClient } from '$lib/api/client';
import type { Track, SongEntry } from '$lib/types';

export class ProjectController {
    isProcessing = $state(false);
    tracks = $state<Track[]>([]);
    globalPitch = $state(0);
    error = $state<string | null>(null);
    sessionId = $state(0);

    // Library state
    library = $state<SongEntry[]>([]);
    isLibraryLoading = $state(false);
    currentSongId = $state<string | null>(null);

    private resetPlayback() {
        this.tracks = [];
        this.sessionId++;
    }

    async handleUpload(file: File | undefined) {
        if (!file) return;

        this.isProcessing = true;
        this.error = null;
        this.resetPlayback();

        try {
            const response = await apiClient.separateAudio(file);
            this.tracks = this.mapResponseToTracks(response.processed_files);
            this.currentSongId = response.job_id;
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
        this.resetPlayback();

        try {
            const response = await apiClient.separateFromURL(url);
            this.tracks = this.mapResponseToTracks(response.processed_files);
            this.currentSongId = response.job_id;
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

        this.error = null;
        this.resetPlayback();
        this.currentSongId = song.id;

        // Use setTimeout to let Svelte destroy old components first
        setTimeout(() => {
            this.tracks = Object.entries(song.stems).map(([name, url]) => ({
                id: crypto.randomUUID(),
                name: name.charAt(0).toUpperCase() + name.slice(1),
                labelKey: ['vocals', 'drums', 'bass', 'other'].includes(name) ? `tracks.${name}` : undefined,
                url,
                isMuted: false,
                volume: 1.0,
                pitch: 0
            }));
            this.sessionId++;
        }, 0);
    }

    async deleteSong(songId: string) {
        try {
            await apiClient.deleteSong(songId);
            this.library = this.library.filter(s => s.id !== songId);
            if (this.currentSongId === songId) {
                this.resetPlayback();
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