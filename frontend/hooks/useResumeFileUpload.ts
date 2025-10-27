import { toast } from "sonner";
import { useCallback } from "react";

import { uploadTex } from "@/libs/api";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { handleLoadingChange } from "@/store/slices/progressSlice";
import { setSessionId, setStep } from "@/store/slices/workflowSlice";
import {
    setOriginalFilename,
    setOriginalLatexContent,
    setSections,
} from "@/store/slices/resumeContentSlice";

const useResumeFileUpload = () => {
    const dispatch = useAppDispatch();

    const selectedModel = useAppSelector(
        (state) => state.modelSelection.selectedModel
    );

    const handleFileUpload = useCallback(
        async (acceptedFiles: File[]) => {
            if (!acceptedFiles.length) return;

            dispatch(
                handleLoadingChange({
                    isLoading: true,
                    progressValue: 10,
                    message: "Uploading resume file...",
                })
            );

            try {
                dispatch(
                    handleLoadingChange({
                        isLoading: true,
                        progressValue: 30,
                        message: "Processing LaTeX content...",
                    })
                );

                const res = await uploadTex(acceptedFiles[0], selectedModel);

                dispatch(
                    handleLoadingChange({
                        isLoading: true,
                        progressValue: 60,
                        message: "Generating AI analysis...",
                    })
                );

                const fileContent = await acceptedFiles[0].text();

                dispatch(
                    handleLoadingChange({
                        isLoading: true,
                        progressValue: 90,
                        message: "Finalizing analysis...",
                    })
                );

                dispatch(setSessionId(res.session_id));
                dispatch(setSections(res.sections));
                dispatch(setOriginalLatexContent(fileContent));
                dispatch(setOriginalFilename(res.original_filename));
                dispatch(setStep("align"));

                dispatch(
                    handleLoadingChange({
                        isLoading: false,
                        progressValue: 100,
                        message: "Upload completed!",
                    })
                );
                toast.success("Resume uploaded and analyzed successfully!");
            } catch (error) {
                console.error("Upload failed:", error);
                dispatch(
                    handleLoadingChange({
                        isLoading: false,
                        progressValue: 0,
                        message: "Upload failed",
                    })
                );
                toast.error("Failed to upload resume. Please try again.");
            }
        },
        [dispatch, selectedModel]
    );

    return handleFileUpload;
};

export default useResumeFileUpload;
