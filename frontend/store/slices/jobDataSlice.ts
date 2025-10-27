import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type InputMethod = "manual" | "file" | null;

export interface JobDataState {
    jobTitle: string;
    jobDescription: string;
    companyName: string;
    inputMethod: InputMethod;
    originalJobFile: File | null;
}

const initialState: JobDataState = {
    jobTitle: "",
    jobDescription: "",
    companyName: "",
    inputMethod: null,
    originalJobFile: null,
};

const jobDataSlice = createSlice({
    name: "jobData",
    initialState,
    reducers: {
        setJobTitle: (state, action: PayloadAction<string>) => {
            state.jobTitle = action.payload;
        },
        setJobDescription: (state, action: PayloadAction<string>) => {
            state.jobDescription = action.payload;
        },
        setCompanyName: (state, action: PayloadAction<string>) => {
            state.companyName = action.payload;
        },
        setInputMethod: (state, action: PayloadAction<InputMethod>) => {
            state.inputMethod = action.payload;
        },
        setOriginalJobFile: (state, action: PayloadAction<File | null>) => {
            state.originalJobFile = action.payload;
        },
        resetJobData: (state) => {
            state.jobTitle = "";
            state.jobDescription = "";
            state.companyName = "";
            state.inputMethod = null;
            state.originalJobFile = null;
        },
    },
});

export const {
    setJobTitle,
    setJobDescription,
    setCompanyName,
    setInputMethod,
    setOriginalJobFile,
    resetJobData,
} = jobDataSlice.actions;
export default jobDataSlice.reducer;
