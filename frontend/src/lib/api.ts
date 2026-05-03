import { browser } from '$app/environment';
import { env as dynamic_env } from '$env/dynamic/public';
import { env as private_env } from '$env/dynamic/private';

const API_URL = browser 
    ? dynamic_env.PUBLIC_PROCESSOR_API_BASE_URL 
    : private_env.INTERNAL_PROCESSOR_URL;

export async function processAudio(fileId: string) {
    const response = await fetch(`${API_URL}/process/${fileId}`, {
        method: 'POST'
    });
    return response.json();
}