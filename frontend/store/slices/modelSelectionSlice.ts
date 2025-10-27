import { createSlice, PayloadAction } from "@reduxjs/toolkit";

import type { AIModel, ModelsResponse } from "@/libs/api";
import { DEFAULT_MODEL } from "@/constants";

interface ModelSelectionState {
    models: AIModel[];
    selectedModel: string;
    sliceProjects: boolean;
    defaultModel: string;
}

const initialState: ModelSelectionState = {
    models: [],
    selectedModel: "",
    sliceProjects: true,
    defaultModel: DEFAULT_MODEL,
};

const modelSelectionSlice = createSlice({
    name: "modelSelection",
    initialState,
    reducers: {
        setModels: (state, action: PayloadAction<AIModel[]>) => {
            state.models = action.payload;
        },
        setSelectedModel: (state, action: PayloadAction<string>) => {
            state.selectedModel = action.payload;
        },
        setSliceProjects: (state, action: PayloadAction<boolean>) => {
            state.sliceProjects = action.payload;
        },
        setDefaultModel: (state, action: PayloadAction<string>) => {
            state.defaultModel = action.payload;
        },
        fetchModelsSuccess: (state, action: PayloadAction<ModelsResponse>) => {
            state.models = action.payload.models;
            state.defaultModel = action.payload.default_model;
            if (!state.selectedModel) {
                state.selectedModel = action.payload.default_model;
            }
        },
        fetchModelsFailure: (state, action: PayloadAction<string>) => {
            state.selectedModel = DEFAULT_MODEL;
            state.defaultModel = DEFAULT_MODEL;
        },
        resetModelSelection: (state) => {
            state.models = [];
            state.selectedModel = "";
            state.defaultModel = DEFAULT_MODEL;
        },
        resetModelConfig: (state) => {
            state.selectedModel = DEFAULT_MODEL;
            state.sliceProjects = true;
        },
    },
});

export const {
    setModels,
    setSelectedModel,
    setSliceProjects,
    setDefaultModel,
    fetchModelsSuccess,
    fetchModelsFailure,
    resetModelSelection,
    resetModelConfig,
} = modelSelectionSlice.actions;
export default modelSelectionSlice.reducer;
