import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ProjectController } from './ProjectController.svelte';
import { apiClient } from '$lib/api/client';
import type { ProcessResponse } from '$lib/types';

vi.mock('$lib/api/client', () => ({
    apiClient: {
        separateAudio: vi.fn(),
        separateFromURL: vi.fn(),
        getAudioUrl: vi.fn((path) => `http://mock-api/${path}`)
    }
}));

describe('ProjectController Business Logic', () => {
    let controller: ProjectController;

    beforeEach(() => {
        controller = new ProjectController();
        vi.clearAllMocks();
    });

    // --- INITIALIZATION ---
    it('should initialize with default empty state and global pitch at 0', () => {
        expect(controller.isProcessing).toBe(false);
        expect(controller.tracks).toHaveLength(0);
        expect(controller.globalPitch).toBe(0);
        expect(controller.error).toBeNull();
    });

    // --- FILE UPLOAD ---
    it('should process upload and map response to tracks correctly', async () => {
        const mockResponse: ProcessResponse = {
            job_id: 'test-job',
            status: 'done',
            processed_files: ['stems/vocals.wav', 'stems/drums.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        const mockFile = new File(['dummy'], 'song.mp3', { type: 'audio/mpeg' });

        const promise = controller.handleUpload(mockFile);
        expect(controller.isProcessing).toBe(true);

        await promise;

        expect(controller.isProcessing).toBe(false);
        expect(controller.error).toBeNull();
        expect(controller.tracks).toHaveLength(2);
        expect(controller.tracks[0].name).toBe('Vocals');
        expect(controller.tracks[1].name).toBe('Drums');
    });

    it('should correctly assign label keys regardless of file name casing', async () => {
        const mockResponse: ProcessResponse = {
            job_id: 'case-test',
            status: 'done',
            processed_files: ['stems/VOCALS.wav', 'stems/BASS.wav', 'stems/unknown_instrument.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        await controller.handleUpload(new File([''], 'test.mp3'));

        expect(controller.tracks[0].labelKey).toBe('tracks.vocals');
        expect(controller.tracks[1].labelKey).toBe('tracks.bass');
        expect(controller.tracks[2].labelKey).toBeUndefined();
    });

    it('should correctly assign label keys with exact stem names only', async () => {
        const mockResponse: ProcessResponse = {
            job_id: 'mapping-test',
            status: 'done',
            processed_files: [
                'stems/VOCALS.wav',
                'stems/Bass.wav',
                'stems/Drums.wav',
                'stems/piano.wav'
            ]
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        await controller.handleUpload(new File([''], 'test.mp3'));

        expect(controller.tracks[0].labelKey).toBe('tracks.vocals');
        expect(controller.tracks[1].labelKey).toBe('tracks.bass');
        expect(controller.tracks[2].labelKey).toBe('tracks.drums');
        expect(controller.tracks[3].labelKey).toBeUndefined();
    });

    // --- PITCH MANAGEMENT ---
    it('should update global pitch correctly and clamp values within [-12, 12]', () => {
        controller.setGlobalPitch(5);
        expect(controller.globalPitch).toBe(5);

        controller.setGlobalPitch(20);
        expect(controller.globalPitch).toBe(12);

        controller.setGlobalPitch(-100);
        expect(controller.globalPitch).toBe(-12);
    });

    it('should clamp global pitch within the safety range [-12, 12]', () => {
        controller.setGlobalPitch(25);
        expect(controller.globalPitch).toBe(12);

        controller.setGlobalPitch(-50);
        expect(controller.globalPitch).toBe(-12);
    });

    it('should maintain global pitch setting after a new file upload', async () => {
        controller.setGlobalPitch(4);

        const mockResponse: ProcessResponse = {
            job_id: 'test-job',
            status: 'done',
            processed_files: ['stems/vocals.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        await controller.handleUpload(new File([''], 'song.mp3'));
        expect(controller.globalPitch).toBe(4);
    });

    // --- STATE INTEGRITY & ERROR HANDLING ---
    it('should clear previous tracks and errors when a new upload starts', async () => {
        controller.error = "Previous failure";
        const mockResponse: ProcessResponse = {
            job_id: 'new-job',
            status: 'done',
            processed_files: ['stems/vocals.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        const uploadPromise = controller.handleUpload(new File([''], 'new.mp3'));

        expect(controller.tracks).toHaveLength(0);
        expect(controller.error).toBeNull();

        await uploadPromise;
        expect(controller.tracks).toHaveLength(1);
    });

    it('should immediately clear previous tracks and errors when a new upload starts', async () => {
        controller.error = "Old Error";
        // @ts-ignore
        controller.tracks = [{ id: 'old-track' }];

        const mockResponse = { job_id: 'new', status: 'done', processed_files: ['stems/v.wav'] };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse as any);

        const uploadPromise = controller.handleUpload(new File([''], 'new.mp3'));

        expect(controller.tracks).toHaveLength(0);
        expect(controller.error).toBeNull();

        await uploadPromise;
    });

    it('should handle API errors while preserving current configuration', async () => {
        controller.setGlobalPitch(-2);
        const errorMessage = 'Internal Server Error';
        vi.mocked(apiClient.separateAudio).mockRejectedValue(new Error(errorMessage));

        await controller.handleUpload(new File(['dummy'], 'song.mp3'));

        expect(controller.isProcessing).toBe(false);
        expect(controller.error).toBe(errorMessage);
        expect(controller.tracks).toHaveLength(0);
        expect(controller.globalPitch).toBe(-2);
    });

    it('should initialize tracks with full volume and unmuted status', async () => {
        const mockResponse: ProcessResponse = {
            job_id: '1',
            status: 'done',
            processed_files: ['stems/vocals.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);
        await controller.handleUpload(new File([''], 'test.mp3'));

        const track = controller.tracks[0];
        expect(track.volume).toBe(1.0);
        expect(track.isMuted).toBe(false);
        expect(track.url).toBe('http://mock-api/stems/vocals.wav');
    });

    it('should initialize tracks with specific individual defaults', async () => {
        const mockResponse = { job_id: '1', status: 'done', processed_files: ['stems/a.wav'] };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse as any);

        await controller.handleUpload(new File([''], 't.mp3'));

        const track = controller.tracks[0];
        expect(track.pitch).toBe(0);
        expect(track.volume).toBe(1.0);
        expect(track.isMuted).toBe(false);
    });

    // --- URL PROCESSING ---
    it('should process a YouTube URL and map response to tracks', async () => {
        const mockResponse: ProcessResponse = {
            job_id: 'url-job',
            status: 'done',
            processed_files: ['stems/vocals.wav', 'stems/drums.wav', 'stems/bass.wav', 'stems/other.wav']
        };
        vi.mocked(apiClient.separateFromURL).mockResolvedValue(mockResponse);

        const promise = controller.handleURL('https://youtube.com/watch?v=test');
        expect(controller.isProcessing).toBe(true);

        await promise;

        expect(controller.isProcessing).toBe(false);
        expect(controller.tracks).toHaveLength(4);
        expect(apiClient.separateFromURL).toHaveBeenCalledWith('https://youtube.com/watch?v=test');
    });

    it('should ignore empty URL strings', async () => {
        await controller.handleURL('');
        expect(controller.isProcessing).toBe(false);
        expect(apiClient.separateFromURL).not.toHaveBeenCalled();

        await controller.handleURL('   ');
        expect(apiClient.separateFromURL).not.toHaveBeenCalled();
    });

    it('should handle URL processing errors gracefully', async () => {
        vi.mocked(apiClient.separateFromURL).mockRejectedValue(new Error('Download failed'));

        await controller.handleURL('https://youtube.com/watch?v=bad');

        expect(controller.isProcessing).toBe(false);
        expect(controller.error).toBe('Download failed');
        expect(controller.tracks).toHaveLength(0);
    });

    it('should clear previous state when a new URL is submitted', async () => {
        controller.error = "Old error";
        // @ts-ignore
        controller.tracks = [{ id: 'old' }];

        const mockResponse: ProcessResponse = {
            job_id: 'new-url',
            status: 'done',
            processed_files: ['stems/vocals.wav']
        };
        vi.mocked(apiClient.separateFromURL).mockResolvedValue(mockResponse);

        const promise = controller.handleURL('https://youtube.com/watch?v=new');

        expect(controller.tracks).toHaveLength(0);
        expect(controller.error).toBeNull();

        await promise;
        expect(controller.tracks).toHaveLength(1);
    });

    it('should preserve global pitch after URL processing', async () => {
        controller.setGlobalPitch(7);

        const mockResponse: ProcessResponse = {
            job_id: 'pitch-test',
            status: 'done',
            processed_files: ['stems/vocals.wav']
        };
        vi.mocked(apiClient.separateFromURL).mockResolvedValue(mockResponse);

        await controller.handleURL('https://youtube.com/watch?v=test');
        expect(controller.globalPitch).toBe(7);
    });
});