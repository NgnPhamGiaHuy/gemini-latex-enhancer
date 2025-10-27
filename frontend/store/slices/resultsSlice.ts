import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface GenerateResult {
    tex?: string;
    pdf?: string | null;
    clean_tex_filename?: string;
    clean_pdf_filename?: string | null;
}

export interface ResultsState {
    generateResult: GenerateResult;
}

const initialState: ResultsState = {
    generateResult: {},
};

const resultsSlice = createSlice({
    name: "results",
    initialState,
    reducers: {
        setGenerateResult: (state, action: PayloadAction<GenerateResult>) => {
            state.generateResult = action.payload;
        },
        resetResults: (state) => {
            state.generateResult = {};
        },
    },
});

export const { setGenerateResult, resetResults } = resultsSlice.actions;
export default resultsSlice.reducer;
