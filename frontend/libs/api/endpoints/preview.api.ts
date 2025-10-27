import { ROUTES } from "../routes";
import { apiClient } from "../core/client";
import { logRequestError } from "../helpers/logging";

import type { PreviewFileResponse } from "../core/types";

export const previewFile = async (file: File): Promise<PreviewFileResponse> => {
    console.log("=== FRONTEND FETCHING PREVIEW FILE ===");

    try {
        const formData = new FormData();
        formData.append("file", file);

        const responseData = await apiClient<PreviewFileResponse>(
            ROUTES.FILE_PREVIEW,
            {
                method: "POST",
                body: formData,
            }
        );

        console.log("✅ Preview file fetched successfully:", responseData);
        return responseData;
    } catch (error) {
        logRequestError("Fetch preview file", error);
        throw error;
    }
};
