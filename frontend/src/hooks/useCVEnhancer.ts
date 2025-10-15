import { useState, useEffect } from "react";

import type { Section } from "@/lib/api";
import type { CVEnhancerState, CVEnhancerActions, Step } from "@/types";

const useCVEnhancer = (): CVEnhancerState & CVEnhancerActions => {
    const [step, setStep] = useState<Step>("upload");
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [summary, setSummary] = useState<string>("");
    const [sections, setSections] = useState<Section[]>([]);
    const [originalLatexContent, setOriginalLatexContent] = useState<string>("");
    const [jobTitle, setJobTitle] = useState("");
    const [jobDescription, setJobDescription] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [sliceProjects, setSliceProjects] = useState(true);
    const [selectedModel, setSelectedModel] = useState<string>("gemini-2.5-flash");
    const [generateResult, setGenerateResult] = useState<{
        tex?: string;
        pdf?: string | null;
    }>({});
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [progressMessage, setProgressMessage] = useState("");
    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
    }, []);

    const handleLoadingChange = (isLoading: boolean, progressValue: number, message: string = "") => {
        setLoading(isLoading);
        setProgress(progressValue);
        setProgressMessage(message);
    };

    const resetState = () => {
        setStep("upload");
        setSessionId(null);
        setSummary("");
        setSections([]);
        setOriginalLatexContent("");
        setJobTitle("");
        setJobDescription("");
        setCompanyName("");
        setSliceProjects(false);
        setSelectedModel("gemini-2.5-flash");
        setGenerateResult({});
        setLoading(false);
        setProgress(0);
        setProgressMessage("");
    };

    return {
        // State
        step,
        sessionId,
        summary,
        sections,
        originalLatexContent,
        jobTitle,
        jobDescription,
        companyName,
        sliceProjects,
        selectedModel,
        generateResult,
        loading,
        progress,
        progressMessage,
        isClient,
        // Actions
        setStep,
        setSessionId,
        setSummary,
        setSections,
        setOriginalLatexContent,
        setJobTitle,
        setJobDescription,
        setCompanyName,
        setSliceProjects,
        setSelectedModel,
        setGenerateResult,
        setLoading,
        setProgress,
        setProgressMessage,
        handleLoadingChange,
        resetState,
    };
};

export default useCVEnhancer;
