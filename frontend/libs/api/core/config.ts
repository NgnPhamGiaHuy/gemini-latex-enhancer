export const API_BASE =
    process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export const buildOutputUrl = (relPath: string): string => {
    return `${API_BASE}/session-outputs/${relPath}`;
};

export const buildDownloadUrl = (
    filename: string,
    downloadName?: string
): string => {
    const url = new URL(`${API_BASE}/api/download/${filename}`);
    if (downloadName) {
        url.searchParams.set("download_name", downloadName);
    }
    return url.toString();
};
