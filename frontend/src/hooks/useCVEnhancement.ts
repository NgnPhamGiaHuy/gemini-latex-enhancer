import { toast } from "sonner";
import { useCallback } from "react";

import { alignSections, alignSectionsBatch, BatchAlignResponse, fetchProgress } from "@/lib/api";

import type { EnhancementParams, UseCVEnhancementProps } from "@/types";

const useCVEnhancement = ({ onEnhanceSuccess, onLoadingChange }: UseCVEnhancementProps) => {
    const handleEnhancement = useCallback(
        async (params: EnhancementParams) => {
            const { sessionId, jobTitle, jobDescription, companyName, originalLatexContent, modelId, sliceProjects } = params;

            if (!sessionId) return;

            // Start loading with progress tracking
            onLoadingChange(true, 10, "Preparing enhancement...");

            try {
                console.log("=== FRONTEND ENHANCE HANDLER STARTED ===");
                console.log("Enhance parameters:", {
                    sessionId,
                    jobTitle,
                    jobDescription,
                    companyName,
                    latexContentLength: originalLatexContent.length,
                    sliceProjects,
                });

                onLoadingChange(true, 30, "Analyzing job requirements...");

                const res = await alignSections({
                    session_id: sessionId,
                    job_title: jobTitle,
                    job_description: jobDescription,
                    company_name: companyName || undefined,
                    latex_content: originalLatexContent,
                    model_id: modelId,
                    slice_projects: sliceProjects,
                });

                onLoadingChange(true, 70, "Generating enhanced CV...");

                console.log("Enhance response received:", res);

                onLoadingChange(true, 90, "Compiling LaTeX to PDF...");

                onEnhanceSuccess({ tex: res.tex_path, pdf: res.pdf_path });

                onLoadingChange(false, 100, "Enhancement completed!");
                toast.success("CV enhanced and ready for download!");
                console.log("=== FRONTEND ENHANCE HANDLER COMPLETED ===");
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
            async (params: { sessionId: string; latexContent: string; csvFile: File; modelId?: string; sliceProjects?: boolean; onProgress?: (current: number, total: number) => void }) => {
                const { sessionId, latexContent, csvFile, modelId, sliceProjects, onProgress } = params;
                if (!sessionId) return;

                onLoadingChange(true, 10, "Preparing batch enhancement...");
                try {
                    // Kick off batch
                    const resPromise = alignSectionsBatch({
                        session_id: sessionId,
                        latex_content: latexContent,
                        csv_file: csvFile,
                        model_id: modelId,
                        slice_projects: sliceProjects,
                    });

                    // Poll progress while backend processes
                    let done = false;
                    // Start with a small delay so we don't stick at 10%
                    await new Promise((r) => setTimeout(r, 600));
                    while (!done) {
                        await new Promise((r) => setTimeout(r, 1000));
                        try {
                            const p = await fetchProgress(sessionId);
                            if (onProgress) onProgress(p.current, p.total);
                            const message = p.message || `Processing ${p.current} of ${p.total}`;
                            // Ensure we never regress; cap at 98% until completion
                            const safePercent = Math.max(15, Math.min(98, p.percent));
                            onLoadingChange(true, safePercent, message);
                            if (p.status === "completed") {
                                done = true;
                            } else if (p.status === "failed") {
                                throw new Error("Batch enhancement failed");
                            }
                        } catch (e) {
                            // Ignore transient errors
                        }
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
