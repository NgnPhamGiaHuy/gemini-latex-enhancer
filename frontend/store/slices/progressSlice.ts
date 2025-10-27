import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface ProgressState {
    loading: boolean;
    progress: number;
    progressMessage: string;
}

const initialState: ProgressState = {
    loading: false,
    progress: 0,
    progressMessage: "",
};

const progressSlice = createSlice({
    name: "progress",
    initialState,
    reducers: {
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setProgress: (state, action: PayloadAction<number>) => {
            state.progress = action.payload;
        },
        setProgressMessage: (state, action: PayloadAction<string>) => {
            state.progressMessage = action.payload;
        },
        handleLoadingChange: (
            state,
            action: PayloadAction<{
                isLoading: boolean;
                progressValue: number;
                message?: string;
            }>
        ) => {
            state.loading = action.payload.isLoading;
            state.progress = action.payload.progressValue;
            state.progressMessage = action.payload.message || "";
        },
        resetProgress: (state) => {
            state.loading = false;
            state.progress = 0;
            state.progressMessage = "";
        },
    },
});

export const {
    setLoading,
    setProgress,
    setProgressMessage,
    handleLoadingChange,
    resetProgress,
} = progressSlice.actions;
export default progressSlice.reducer;
