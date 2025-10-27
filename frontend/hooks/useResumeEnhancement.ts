"use client";

import { toast } from "sonner";
import { useCallback } from "react";

import { alignSections } from "@/libs/api";
import { useAppSelector } from "@/store/hooks";

import { EnhanceSuccessData } from "@/types";

interface UseResumeEnhancementProps {
    onEnhanceSuccess: (data: EnhanceSuccessData) => void;
    onLoadingChange: (
        isLoading: boolean,
        progressValue: number,
        message?: string
    ) => void;
}

const useResumeEnhancement = ({
    onEnhanceSuccess,
    onLoadingChange,
}: UseResumeEnhancementProps) => {
    const sessionId = useAppSelector((state) => state.workflow.sessionId);

    const jobTitle = useAppSelector((state) => state.jobData.jobTitle);
    const jobDescription = useAppSelector(
        (state) => state.jobData.jobDescription
    );
    const companyName = useAppSelector((state) => state.jobData.companyName);
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

    const handleEnhancement = useCallback(async () => {
        if (!sessionId) {
            toast.error("Session ID is required for enhancement");
            return;
        }

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
                model_id: selectedModel,
                slice_projects: sliceProjects,
            });

            onLoadingChange(true, 70, "Generating enhanced CV...");
            onLoadingChange(true, 90, "Compiling LaTeX to PDF...");

            onEnhanceSuccess({
                tex: res.tex_path,
                pdf: res.pdf_path,
                clean_tex_filename: res.clean_tex_filename,
                clean_pdf_filename: res.clean_pdf_filename,
            });

            onLoadingChange(false, 100, "Enhancement completed!");
            toast.success("CV enhanced and ready for download!");
        } catch (error) {
            console.error("Align failed:", error);
            onLoadingChange(false, 0, "Enhancement failed");
            toast.error("Failed to enhance CV. Please try again.");
        }
    }, [
        onEnhanceSuccess,
        onLoadingChange,
        sessionId,
        jobTitle,
        jobDescription,
        companyName,
        originalLatexContent,
        originalFilename,
        selectedModel,
        sliceProjects,
    ]);

    return handleEnhancement;
};

export default useResumeEnhancement;
