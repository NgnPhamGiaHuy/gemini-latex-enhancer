import { ROUTES } from "../routes";
import { apiClient } from "../core/client";
import { logRequestError, logRequestStart } from "../helpers/logging";

import type { UploadResponse } from "../core/types";

export const uploadTex = async (
    file: File,
    modelId?: string
): Promise<UploadResponse> => {
    logRequestStart("FRONTEND UPLOAD STARTED", {
        "File name": file.name,
        "File size": file.size,
        "File type": file.type,
        "Selected model": modelId || "default",
    });

    const form = new FormData();
    form.append("file", file);

    if (modelId) {
        form.append("model_id", modelId);
    }

    console.log("FormData created, sending request to:", ROUTES.UPLOAD);

    try {
        const responseData = await apiClient<UploadResponse>(ROUTES.UPLOAD, {
            method: "POST",
            body: form,
        });

        console.log("✅ Upload successful, response data:", responseData);
        console.log("=== FRONTEND UPLOAD COMPLETED ===");

        console.log("Data summary:", {
            session_id: responseData.session_id,
            sections_count: responseData.sections?.length || 0,
        });

        return responseData;
    } catch (error) {
        logRequestError("Upload", error);
        throw error;
    }
};
