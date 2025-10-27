import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type Step = "upload" | "align" | "download";

export interface WorkflowState {
    step: Step;
    sessionId: string | null;
}

const initialState: WorkflowState = {
    step: "upload",
    sessionId: null,
};

const workflowSlice = createSlice({
    name: "workflow",
    initialState,
    reducers: {
        setStep: (state, action: PayloadAction<Step>) => {
            state.step = action.payload;
        },
        setSessionId: (state, action: PayloadAction<string | null>) => {
            state.sessionId = action.payload;
        },
        resetWorkflow: (state) => {
            state.step = "upload";
            state.sessionId = null;
        },
    },
});

export const { setStep, setSessionId, resetWorkflow } = workflowSlice.actions;
export default workflowSlice.reducer;
