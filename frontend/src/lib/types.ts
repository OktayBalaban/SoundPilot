export interface ProcessResponse {
    job_id: string;
    status: string;
    processed_files: string[];
}

export interface Track {
    id: string;
    name: string;
    url: string;
    isMuted: boolean;
    volume: number;
}