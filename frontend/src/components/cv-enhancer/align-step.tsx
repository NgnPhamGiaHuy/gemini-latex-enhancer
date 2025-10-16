"use client";

import { motion } from "framer-motion";

import type { AlignStepProps } from "@/types";

import AIAnalysis from "./ai-analysis";
import JobDetailsForm from "./job-details-form";
import { useCVEnhancement } from "@/hooks";

const AlignStep = ({ step, summary, jobTitle, setJobTitle, jobDescription, setJobDescription, companyName, setCompanyName, sliceProjects, setSliceProjects, selectedModel, onEnhanceSuccess, onLoadingChange, sessionId, originalLatexContent }: AlignStepProps) => {
    const { handleEnhancement, handleBatchEnhancement } = useCVEnhancement({
        onEnhanceSuccess,
        onLoadingChange,
    });

    const handleEnhance = () => {
        if (!sessionId) return;

        handleEnhancement({ sessionId, jobTitle, jobDescription, companyName, originalLatexContent, modelId: selectedModel, sliceProjects });
    };

    if (step !== "align") return null;

    return (
        <motion.div key="align" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} transition={{ duration: 0.4 }}>
            <div className="grid lg:grid-cols-2 gap-8">
                <AIAnalysis summary={summary} loading={false} />
                <JobDetailsForm
                    jobTitle={jobTitle}
                    setJobTitle={setJobTitle}
                    jobDescription={jobDescription}
                    setJobDescription={setJobDescription}
                    companyName={companyName}
                    setCompanyName={setCompanyName}
                    sliceProjects={sliceProjects}
                    setSliceProjects={setSliceProjects}
                    onEnhance={handleEnhance}
                    onBatchEnhance={async ({ csvFile }) => {
                        if (!sessionId) return;
                        const res = await handleBatchEnhancement({
                            sessionId,
                            latexContent: originalLatexContent,
                            csvFile,
                            modelId: selectedModel,
                            sliceProjects,
                        });
                        // After batch completes, move to download step with zip only
                        onEnhanceSuccess({ tex: res?.zip_path });
                    }}
                    loading={false}
                />
            </div>
        </motion.div>
    );
};

export default AlignStep;
