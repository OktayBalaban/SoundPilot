export interface Track {
    name: string;
    url: string;
    isMuted: boolean;
    volume: number;
}

export interface ProcessResponse {
    job_id: string;
    status: string;
    processed_files: string[];
}