import { useState, useEffect, useCallback } from "react";

import { fetchAvailableModels, type ModelsResponse } from "@/libs/api";
import { useDispatch } from "react-redux";
import {
    setDefaultModel,
    setModels,
    setSelectedModel,
} from "@/store/slices/modelSelectionSlice";
import { useAppSelector } from "@/store/hooks";
import { DEFAULT_MODEL } from "@/constants";

interface UseModelSelectionReturn {
    models: Array<{
        id: string;
        name: string;
        description: string;
        provider: string;
        default: boolean;
    }>;
    selectedModel: string;
    defaultModel: string;
    isLoading: boolean;
    error: string | null;
}

const useModelSelection = (): UseModelSelectionReturn => {
    const dispatch = useDispatch();

    const { models, selectedModel, defaultModel } = useAppSelector(
        (state) => state.modelSelection
    );

    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    const fetchModels = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);

            const response: ModelsResponse = await fetchAvailableModels();

            dispatch(setModels(response.models));
            dispatch(setDefaultModel(response.default_model));

            const currentSelectedModel = selectedModel || "";
            if (!currentSelectedModel) {
                dispatch(setSelectedModel(response.default_model));
            }
        } catch (err) {
            const errorMessage =
                err instanceof Error ? err.message : "Failed to fetch models";
            console.error("❌ Failed to fetch models:", errorMessage);
            setError(errorMessage);

            dispatch(setSelectedModel(DEFAULT_MODEL));
            dispatch(setDefaultModel(DEFAULT_MODEL));
        } finally {
            setIsLoading(false);
        }
    }, [dispatch, selectedModel]);

    useEffect(() => {
        fetchModels();
    }, [fetchModels]);

    return {
        models,
        selectedModel,
        defaultModel,
        isLoading,
        error,
    };
};

export default useModelSelection;
