import { useState, useEffect, useCallback } from "react";

import type { UseModelSelectionProps, UseModelSelectionReturn } from "@/types";

import {
    fetchAvailableModels,
    type AIModel,
    type ModelsResponse,
} from "@/lib/api";

const useModelSelection = ({
    onModelChange,
}: UseModelSelectionProps = {}): UseModelSelectionReturn => {
    const [models, setModels] = useState<AIModel[]>([]);
    const [selectedModel, setSelectedModelState] = useState<string>("");
    const [defaultModel, setDefaultModel] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchModels = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);

            const response: ModelsResponse = await fetchAvailableModels();

            setModels(response.models);
            setDefaultModel(response.default_model);

            if (!selectedModel) {
                setSelectedModelState(response.default_model);
                onModelChange?.(response.default_model);
            }
        } catch (err) {
            const errorMessage =
                err instanceof Error ? err.message : "Failed to fetch models";
            console.error("❌ Failed to fetch models:", errorMessage);
            setError(errorMessage);

            // Fallback to default model
            const fallbackModel = "gemini-2.5-flash";
            setSelectedModelState(fallbackModel);
            setDefaultModel(fallbackModel);
            onModelChange?.(fallbackModel);
        } finally {
            setIsLoading(false);
        }
    }, [selectedModel, onModelChange]);

    const setSelectedModel = useCallback(
        (modelId: string) => {
            setSelectedModelState(modelId);
            onModelChange?.(modelId);
        },
        [selectedModel, onModelChange]
    );

    const refreshModels = useCallback(async () => {
        await fetchModels();
    }, [fetchModels]);

    useEffect(() => {
        fetchModels();
    }, [fetchModels]);

    return {
        models,
        selectedModel,
        defaultModel,
        isLoading,
        error,
        setSelectedModel,
        refreshModels,
    };
};

export default useModelSelection;
