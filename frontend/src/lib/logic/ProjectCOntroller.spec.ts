import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ProjectController } from './ProjectController.svelte';
import { apiClient } from '$lib/api/client';

// Mock the API client to avoid real network requests
vi.mock('$lib/api/client', () => ({
    apiClient: {
        separateAudio: vi.fn(),
        getAudioUrl: vi.fn((path) => `http://mock-api/${path}`)
    }
}));

describe('ProjectController Business Logic', () => {
    let controller: ProjectController;

    beforeEach(() => {
        // Reset controller state before each test
        controller = new ProjectController();
        vi.clearAllMocks();
    });

    it('should initialize with default empty state', () => {
        expect(controller.isProcessing).toBe(false);
        expect(controller.tracks).toHaveLength(0);
        expect(controller.error).toBeNull();
    });

    it('should process upload and map response to tracks successfully', async () => {
        // Setup mock response
        const mockResponse = {
            job_id: 'test-job',
            status: 'done',
            processed_files: ['stems/vocals.wav', 'stems/drums.wav']
        };
        vi.mocked(apiClient.separateAudio).mockResolvedValue(mockResponse);

        const mockFile = new File(['dummy'], 'song.mp3', { type: 'audio/mpeg' });
        
        // Execute action
        const promise = controller.handleUpload(mockFile);
        
        // Assert: Processing state should be true immediately
        expect(controller.isProcessing).toBe(true);

        await promise;

        // Assert: Final state after success
        expect(controller.isProcessing).toBe(false);
        expect(controller.error).toBeNull();
        expect(controller.tracks).toHaveLength(2);
        expect(controller.tracks[0].name).toBe('Vocals'); // Should capitalize
        expect(controller.tracks[0].url).toBe('http://mock-api/stems/vocals.wav');
    });

    it('should handle API errors correctly', async () => {
        // Setup mock error
        const errorMessage = 'Network Failed';
        vi.mocked(apiClient.separateAudio).mockRejectedValue(new Error(errorMessage));

        const mockFile = new File(['dummy'], 'song.mp3');

        // Execute action
        await controller.handleUpload(mockFile);

        // Assert: Error state
        expect(controller.isProcessing).toBe(false);
        expect(controller.error).toBe(errorMessage);
        expect(controller.tracks).toHaveLength(0);
    });
});