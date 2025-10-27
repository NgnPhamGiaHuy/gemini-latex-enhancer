export class ApiError extends Error {
    constructor(
        public status: number,
        public statusText: string,
        message?: string
    ) {
        super(message || `API request failed: ${status} ${statusText}`);
        this.name = "ApiError";
    }
}

export function handleApiError(res: Response, context: string): never {
    throw new ApiError(res.status, res.statusText, `${context} failed`);
}
