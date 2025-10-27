import { ROUTES } from "../routes";
import { apiClient } from "../core/client";
import { logRequestError } from "../helpers/logging";

import type { AIModel, ModelsResponse } from "../core/types";

export const fetchAvailableModels = async (): Promise<ModelsResponse> => {
    console.log("=== FRONTEND FETCHING MODELS ===");

    try {
        const responseData = await apiClient<{
            models: AIModel[];
            default_model: string;
        }>(ROUTES.MODELS, { cache: "no-cache" });

        console.log("✅ Models fetched successfully:", responseData);
        return responseData;
    } catch (error) {
        logRequestError("Fetch models", error);
        throw error;
    }
};
