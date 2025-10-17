"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

import AlignStep from "./align-step";
import UploadStep from "./upload-step";
import DownloadStep from "./download-step";
import { StepIndicator } from "@/components/ui/step-indicator";
import { FullScreenProgress } from "@/components/ui/fullscreen-progress";
import { getProgressTitle, getProgressSubtitle, STEPS } from "@/constants/enhancer";
import { useClientSide, useCVEnhancement, useEnhancerWorkflow, useEnhancerJobData, useEnhancerProgress, useEnhancerModelConfig, useEnhancerResults, useEnhancerCVContent } from "@/hooks";

const CVEnhancer = () => {
    const isClient = useClientSide();
    const { step, sessionId, setStep, setSessionId, resetWorkflow } = useEnhancerWorkflow();
    const { summary, originalLatexContent, setSummary, setSections, setOriginalLatexContent, resetCVContent } = useEnhancerCVContent();
    const { jobTitle, jobDescription, companyName, inputMethod, originalJobFile, setJobTitle, setJobDescription, setCompanyName, setInputMethod, setOriginalJobFile, resetJobData } = useEnhancerJobData();
    const { selectedModel, sliceProjects, setSelectedModel, setSliceProjects, resetModelConfig } = useEnhancerModelConfig();
    const { generateResult, setGenerateResult, resetResults } = useEnhancerResults();
    const { loading, progress, progressMessage, handleLoadingChange, resetProgress } = useEnhancerProgress();

    const { handleEnhancement: regenerateEnhancement, handleBatchEnhancement: regenerateBatchEnhancement } = useCVEnhancement({
        onEnhanceSuccess: (result) => {
            setGenerateResult(result);
            setStep("download");
        },
        onLoadingChange: handleLoadingChange,
    });

    if (!isClient) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
            <div className="container mx-auto px-4 py-8 max-w-7xl">
                {/* Header */}
                <motion.div className="text-center mb-8" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
                    <div className="flex items-center justify-center gap-3 mb-4">
                        <motion.div animate={{ rotate: [0, 5, -5, 0] }} transition={{ duration: 2, repeat: Infinity }}>
                            <Sparkles className="h-8 w-8 text-primary" />
                        </motion.div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">CV-Align AI</h1>
                    </div>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">Transform your LaTeX CV with AI-powered optimization tailored to any job description</p>
                </motion.div>

                {/* Progress Indicator */}
                <motion.div className="mb-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.2 }}>
                    <StepIndicator steps={STEPS} currentStep={step} />
                </motion.div>

                {/* Main Content */}
                <UploadStep
                    step={step}
                    selectedModel={selectedModel}
                    onUploadSuccess={(data) => {
                        setSessionId(data.sessionId);
                        setSummary(data.summary);
                        setSections(data.sections);
                        setOriginalLatexContent(data.latexContent);
                        setStep("align");
                    }}
                    onLoadingChange={handleLoadingChange}
                    onModelChange={setSelectedModel}
                />

                <AlignStep
                    step={step}
                    summary={summary}
                    jobTitle={jobTitle}
                    setJobTitle={setJobTitle}
                    jobDescription={jobDescription}
                    setJobDescription={setJobDescription}
                    companyName={companyName}
                    setCompanyName={setCompanyName}
                    sliceProjects={sliceProjects}
                    setSliceProjects={setSliceProjects}
                    selectedModel={selectedModel}
                    onEnhanceSuccess={(result) => {
                        setGenerateResult(result);
                        setStep("download");
                        setInputMethod("manual");
                    }}
                    onLoadingChange={handleLoadingChange}
                    sessionId={sessionId}
                    originalLatexContent={originalLatexContent}
                    onBatchJobDetailsExtracted={(jobDetails) => {
                        setJobTitle(jobDetails.jobTitle);
                        setJobDescription(jobDetails.jobDescription);
                        setCompanyName(jobDetails.companyName);
                    }}
                    onBatchEnhancementSuccess={(result, jobFile) => {
                        setGenerateResult(result);
                        setStep("download");
                        setInputMethod("file");
                        setOriginalJobFile(jobFile);
                    }}
                />

                <DownloadStep
                    step={step}
                    generateResult={generateResult}
                    onStartOver={() => {
                        resetWorkflow();
                        resetCVContent();
                        resetJobData();
                        resetModelConfig();
                        resetResults();
                        resetProgress();
                    }}
                    onBackToJobDetails={() => {
                        // Keep uploaded CV and AI summary/sections, clear job-specific inputs and results
                        resetResults();
                        resetProgress();
                        resetJobData();
                        setSliceProjects(true);
                        setStep("align");
                    }}
                    inputMethod={inputMethod}
                    onRegenerateSingle={async () => {
                        if (!sessionId) return;
                        await regenerateEnhancement({
                            sessionId,
                            jobTitle,
                            jobDescription,
                            companyName,
                            originalLatexContent,
                            modelId: selectedModel,
                            sliceProjects,
                        });
                    }}
                    onRegenerateBatch={async () => {
                        if (!sessionId || !originalJobFile) return;
                        await regenerateBatchEnhancement({
                            sessionId,
                            latexContent: originalLatexContent,
                            jobFile: originalJobFile,
                            modelId: selectedModel,
                            sliceProjects,
                        });
                    }}
                />

                {/* Full Screen Progress Overlay */}
                <FullScreenProgress loading={loading} progress={progress} message={progressMessage} title={getProgressTitle(progressMessage)} subtitle={getProgressSubtitle(progressMessage)} />
            </div>
        </div>
    );
};

export default CVEnhancer;
