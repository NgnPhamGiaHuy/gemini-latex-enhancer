import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { Section } from "@/libs/api";

export interface ResumeContentState {
    originalLatexContent: string;
    sections: Section[];
    originalFilename: string;
}

const initialState: ResumeContentState = {
    originalLatexContent: "",
    sections: [],
    originalFilename: "",
};

const resumeContentSlice = createSlice({
    name: "resumeContent",
    initialState,
    reducers: {
        setOriginalLatexContent: (state, action: PayloadAction<string>) => {
            state.originalLatexContent = action.payload;
        },
        setSections: (state, action: PayloadAction<Section[]>) => {
            state.sections = action.payload;
        },
        setOriginalFilename: (state, action: PayloadAction<string>) => {
            state.originalFilename = action.payload;
        },
        resetResumeContent: (state) => {
            state.originalLatexContent = "";
            state.sections = [];
            state.originalFilename = "";
        },
    },
});

export const {
    setOriginalLatexContent,
    setSections,
    setOriginalFilename,
    resetResumeContent,
} = resumeContentSlice.actions;
export default resumeContentSlice.reducer;
