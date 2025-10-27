import { API_BASE } from "./config";
import { ApiError } from "./error";

export interface FetchOptions extends RequestInit {
    skipAuth?: boolean;
}

export async function apiClient<T>(
    endpoint: string,
    options: FetchOptions = {}
): Promise<T> {
    const { skipAuth, ...fetchOptions } = options;

    const url = endpoint.startsWith("http")
        ? endpoint
        : `${API_BASE}${endpoint}`;

    console.log(`Fetching: ${url}`);
    console.log("Options:", fetchOptions.method || "GET");

    const res = await fetch(url, fetchOptions);

    console.log("Response status:", res.status);
    console.log("Response ok:", res.ok);

    if (!res.ok) {
        const errorText = await res.text();
        console.error(`❌ API request failed:`, errorText);
        throw new ApiError(res.status, res.statusText);
    }

    const data = await res.json();

    if (data.success && data.data) {
        console.log(`✅ API request successful`);
        return data.data;
    } else {
        throw new Error("Invalid response format from server");
    }
}
