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