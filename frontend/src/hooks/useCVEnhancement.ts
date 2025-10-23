import { toast } from "sonner";
import { useCallback } from "react";

import {
    alignSections,
    alignSectionsBatch,
    BatchAlignResponse,
    fetchProgress,
    previewFile,
} from "@/lib/api";

import type { EnhancementParams, UseCVEnhancementProps } from "@/types";

const extractJobDetailsFromPreview = (preview: {
    headers: string[];
    rows: string[][];
}) => {
    const { headers, rows } = preview;

    if (!headers.length || !rows.length) return null;

    const firstRow = rows[0];

    const jobTitleIndex = findFieldIndex(headers, [
        "title",
        "position",
        "role",
        "job",
    ]);
    const jobDescIndex = findFieldIndex(headers, [
        "description",
        "desc",
        "responsibilities",
        "duties",
    ]);
    const companyIndex = findFieldIndex(headers, [
        "company",
        "employer",
        "organization",
        "firm",
    ]);

    if (jobTitleIndex === -1 || jobDescIndex === -1) {
        return null; // Required fields missing
    }

    return {
        jobTitle: firstRow[jobTitleIndex] || "",
        jobDescription: firstRow[jobDescIndex] || "",
        companyName: companyIndex >= 0 ? firstRow[companyIndex] || "" : "",
    };
};

const findFieldIndex = (headers: string[], keywords: string[]): number => {
    for (let i = 0; i < headers.length; i++) {
        const headerLower = headers[i].toLowerCase();
        if (keywords.some((keyword) => headerLower.includes(keyword))) {
            return i;
        }
    }
    return -1;
};

const useCVEnhancement = ({
    onEnhanceSuccess,
    onLoadingChange,
}: UseCVEnhancementProps) => {
    const handleEnhancement = useCallback(
        async (params: EnhancementParams) => {
            const {
                sessionId,
                jobTitle,
                jobDescription,
                companyName,
                originalLatexContent,
                originalFilename,
                modelId,
                sliceProjects,
            } = params;

            if (!sessionId) return;

            onLoadingChange(true, 10, "Preparing enhancement...");

            try {
                onLoadingChange(true, 30, "Analyzing job requirements...");

                const res = await alignSections({
                    session_id: sessionId,
                    job_title: jobTitle,
                    job_description: jobDescription,
                    company_name: companyName || undefined,
                    latex_content: originalLatexContent,
                    original_filename: originalFilename,
                    model_id: modelId,
                    slice_projects: sliceProjects,
                });

                onLoadingChange(true, 70, "Generating enhanced CV...");
                onLoadingChange(true, 90, "Compiling LaTeX to PDF...");

                onEnhanceSuccess({ tex: res.tex_path, pdf: res.pdf_path });

                onLoadingChange(false, 100, "Enhancement completed!");
                toast.success("CV enhanced and ready for download!");
            } catch (error) {
                console.error("Align failed:", error);
                onLoadingChange(false, 0, "Enhancement failed");
                toast.error("Failed to enhance CV. Please try again.");
            }
        },
        [onEnhanceSuccess, onLoadingChange]
    );

    return {
        handleEnhancement,
        handleBatchEnhancement: useCallback(
            async (params: {
                sessionId: string;
                latexContent: string;
                originalFilename?: string;
                jobFile: File;
                modelId?: string;
                sliceProjects?: boolean;
                onProgress?: (current: number, total: number) => void;
                onJobDetailsExtracted?: (jobDetails: {
                    jobTitle: string;
                    jobDescription: string;
                    companyName: string;
                }) => void;
            }) => {
                const {
                    sessionId,
                    latexContent,
                    originalFilename,
                    jobFile,
                    modelId,
                    sliceProjects,
                    onProgress,
                    onJobDetailsExtracted,
                } = params;
                if (!sessionId) return;

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
                        latex_content: latexContent,
                        original_filename: originalFilename,
                        job_file: jobFile,
                        model_id: modelId,
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
            [onLoadingChange]
        ),
    };
};

export default useCVEnhancement;
