import { ROUTES } from "../routes";
import { apiClient } from "../core/client";
import { logRequestError } from "../helpers/logging";

import type { ProgressResponse } from "../core/types";

export const fetchProgress = async (
    session_id: string
): Promise<ProgressResponse> => {
    console.log("=== FRONTEND FETCHING PROGRESS ===");

    try {
        const ts = Date.now();
        const url = `${ROUTES.PROGRESS}?session_id=${encodeURIComponent(session_id)}&ts=${ts}`;
        console.log("Fetching progress from:", url);

        const data = await apiClient<ProgressResponse>(url, {
            cache: "no-cache",
        });

        console.log("✅ Progress fetched successfully:", data);
        return data;
    } catch (error) {
        logRequestError("Fetch progress", error);
        throw error;
    }
};
