export interface Track {
    id: string;
    name: string;
    labelKey?: string;
    url: string;
    isMuted: boolean;
    volume: number;
    pitch: number;
}

export interface ProcessResponse {
    job_id: string;
    status: string;
    processed_files: string[];
}

export interface SongEntry {
    id: string;
    title: string;
    source_url: string;
    created_at: string;
    is_valid: boolean;
    missing_stems: string[];
    stems: Record<string, string>;
}

export interface LibraryResponse {
    songs: SongEntry[];
    total: number;
}