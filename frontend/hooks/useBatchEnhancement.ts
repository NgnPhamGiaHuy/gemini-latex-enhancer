import { useCallback } from "react";

import {
    alignSectionsBatch,
    BatchAlignResponse,
    fetchProgress,
    previewFile,
} from "@/libs/api";

import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { extractJobDetailsFromPreview } from "@/utils";
import {
    setCompanyName,
    setInputMethod,
    setJobDescription,
    setJobTitle,
} from "@/store/slices/jobDataSlice";
import { setGenerateResult } from "@/store/slices/resultsSlice";
import { setStep } from "@/store/slices/workflowSlice";

interface UseBatchEnhancementProps {
    onLoadingChange: (
        isLoading: boolean,
        progressValue: number,
        message?: string
    ) => void;
}

const useBatchEnhancement = ({ onLoadingChange }: UseBatchEnhancementProps) => {
    const dispatch = useAppDispatch();

    const sessionId = useAppSelector((state) => state.workflow.sessionId);
    const originalLatexContent = useAppSelector(
        (state) => state.resumeContent.originalLatexContent
    );
    const originalFilename = useAppSelector(
        (state) => state.resumeContent.originalFilename
    );
    const selectedModel = useAppSelector(
        (state) => state.modelSelection.selectedModel
    );
    const sliceProjects = useAppSelector(
        (state) => state.modelSelection.sliceProjects
    );

    const handleBatchEnhancement = useCallback(
        async (params: {
            jobFile: File;
            onProgress?: (current: number, total: number) => void;
            onJobDetailsExtracted?: (jobDetails: {
                jobTitle: string;
                jobDescription: string;
                companyName: string;
            }) => void;
        }) => {
            const { jobFile, onProgress, onJobDetailsExtracted } = params;

            if (!sessionId) {
                throw new Error("Session ID is required for enhancement");
            }

            onLoadingChange(true, 10, "Preparing batch enhancement...");
            try {
                if (onJobDetailsExtracted) {
                    try {
                        const preview = await previewFile(jobFile);

                        if (
                            preview?.headers &&
                            preview?.rows &&
                            preview.rows.length > 0
                        ) {
                            const jobDetails =
                                extractJobDetailsFromPreview(preview);
                            if (jobDetails) {
                                onJobDetailsExtracted(jobDetails);
                            }
                        }
                    } catch (e) {
                        console.warn(
                            "Failed to extract job details for regeneration:",
                            e
                        );
                    }
                }

                const resPromise = alignSectionsBatch({
                    session_id: sessionId,
                    latex_content: originalLatexContent,
                    original_filename: originalFilename,
                    job_file: jobFile,
                    model_id: selectedModel,
                    slice_projects: sliceProjects,
                });

                let done = false;
                await new Promise((r) => setTimeout(r, 600));
                while (!done) {
                    await new Promise((r) => setTimeout(r, 1000));
                    try {
                        const p = await fetchProgress(sessionId);
                        if (onProgress) onProgress(p.current, p.total);
                        const message =
                            p.message ||
                            `Processing ${p.current} of ${p.total}`;
                        const safePercent = Math.max(
                            15,
                            Math.min(98, p.percent)
                        );
                        onLoadingChange(true, safePercent, message);
                        if (p.status === "completed") {
                            done = true;
                        } else if (p.status === "failed") {
                            throw new Error("Batch enhancement failed");
                        }
                    } catch (e) {}
                }

                const res: BatchAlignResponse = await resPromise;
                onLoadingChange(false, 100, "Batch enhancement completed!");
                return res;
            } catch (error) {
                console.error("Batch enhance failed:", error);
                onLoadingChange(false, 0, "Batch enhancement failed");
                throw error;
            }
        },
        [
            onLoadingChange,
            sessionId,
            originalLatexContent,
            originalFilename,
            selectedModel,
            sliceProjects,
        ]
    );

    const handleBatchEnhance = async ({ jobFile }: { jobFile: File }) => {
        const res = await handleBatchEnhancement({
            jobFile,
            onJobDetailsExtracted: (jobDetails) => {
                dispatch(setJobTitle(jobDetails.jobTitle));
                dispatch(setJobDescription(jobDetails.jobDescription));
                dispatch(setCompanyName(jobDetails.companyName));
            },
        });

        const result = { tex: res?.zip_path };

        dispatch(setGenerateResult(result));
        dispatch(setStep("download"));
        dispatch(setInputMethod("file"));
    };

    return { handleBatchEnhancement, handleBatchEnhance };
};

export default useBatchEnhancement;
