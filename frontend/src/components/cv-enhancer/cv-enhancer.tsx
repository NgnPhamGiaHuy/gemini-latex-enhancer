"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

import AlignStep from "./align-step";
import UploadStep from "./upload-step";
import DownloadStep from "./download-step";
import { StepIndicator } from "@/components/ui/step-indicator";
import { FullScreenProgress } from "@/components/ui/fullscreen-progress";

import { useCVEnhancer, useClientSide, useCVEnhancement } from "@/hooks";
import type { Step } from "@/types";

function getProgressTitle(message: string): string {
    if (message.includes("Preparing")) return "Preparing Enhancement";
    if (message.includes("Analyzing")) return "Analyzing Job Requirements";
    if (message.includes("Generating")) return "Generating Enhanced CV";
    if (message.includes("Compiling")) return "Compiling LaTeX to PDF";
    if (message.includes("completed")) return "Enhancement Complete!";
    if (message.includes("failed")) return "Enhancement Failed";
    return "Enhancing Your CV";
}

function getProgressSubtitle(message: string): string {
    if (message.includes("Preparing")) return "Setting up AI processing pipeline...";
    if (message.includes("Analyzing")) return "Extracting key requirements and skills from job description...";
    if (message.includes("Generating")) return "AI is optimizing your CV content to match job requirements...";
    if (message.includes("Compiling")) return "Converting enhanced LaTeX to PDF format...";
    if (message.includes("completed")) return "Your CV is ready for download!";
    if (message.includes("failed")) return "Something went wrong. Please try again.";
    return "AI is analyzing and optimizing your CV to match the job requirements";
}

const STEPS = [
    { id: "upload", title: "Upload CV", description: "Upload your LaTeX CV" },
    { id: "align", title: "Job Details", description: "Enter target job info" },
    { id: "download", title: "Download", description: "Get your tailored CV" },
] as const satisfies readonly {
    id: Step;
    title: string;
    description: string;
}[];

const CVEnhancer = () => {
    const isClient = useClientSide();
    const { step, sessionId, summary, originalLatexContent, jobTitle, jobDescription, companyName, sliceProjects, selectedModel, generateResult, loading, progress, progressMessage, setStep, setSessionId, setSummary, setSections, setOriginalLatexContent, setJobTitle, setJobDescription, setCompanyName, setSliceProjects, setSelectedModel, setGenerateResult, handleLoadingChange, resetState, resetForNewJob } = useCVEnhancer();

    // Create a regenerate handler that reuses current inputs
    const { handleEnhancement: regenerateEnhancement } = useCVEnhancement({
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
                    }}
                    onLoadingChange={handleLoadingChange}
                    sessionId={sessionId}
                    originalLatexContent={originalLatexContent}
                />

                <DownloadStep
                    step={step}
                    generateResult={generateResult}
                    onStartOver={resetState}
                    onStartAgain={async () => {
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
                    onBackToJobDetails={() => {
                        resetForNewJob();
                    }}
                />

                {/* Full Screen Progress Overlay */}
                <FullScreenProgress loading={loading} progress={progress} message={progressMessage} title={getProgressTitle(progressMessage)} subtitle={getProgressSubtitle(progressMessage)} />
            </div>
        </div>
    );
};

export default CVEnhancer;
