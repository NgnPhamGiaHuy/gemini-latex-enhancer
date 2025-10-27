import { configureStore } from "@reduxjs/toolkit";

// Import all slices
import clientReducer from "./slices/clientSlice";
import resumeContentReducer from "./slices/resumeContentSlice";
import jobDataReducer from "./slices/jobDataSlice";
import modelSelectionReducer from "./slices/modelSelectionSlice";
import progressReducer from "./slices/progressSlice";
import resultsReducer from "./slices/resultsSlice";
import workflowReducer from "./slices/workflowSlice";

const store = configureStore({
    reducer: {
        client: clientReducer,
        // Application workflow and session state
        workflow: workflowReducer,
        // Resume content and sections
        resumeContent: resumeContentReducer,
        // Job posting details
        jobData: jobDataReducer,
        // AI model selection and fetching
        modelSelection: modelSelectionReducer,
        // Progress and loading state
        progress: progressReducer,
        // Enhancement results
        results: resultsReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // File objects can't be serialized, so we ignore them
                ignoredActions: [],
                ignoredActionsPaths: ["payload"],
                ignoredPaths: ["jobData.originalJobFile"],
            },
        }),
});

export { store };
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
