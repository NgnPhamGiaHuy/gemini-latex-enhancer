import type { Section } from "@/libs/api";

// ===== Upload Success Types =====
export interface UploadSuccessData {
    sessionId: string;
    sections: Section[];
    latexContent: string;
    originalFilename: string;
}

// ===== Enhancement Types =====
export interface EnhancementParams {
    sessionId: string;
    jobTitle: string;
    jobDescription: string;
    companyName?: string;
    originalLatexContent: string;
    originalFilename?: string;
    modelId?: string;
    sliceProjects?: boolean;
}

export interface EnhanceSuccessData {
    tex?: string;
    pdf?: string | null;
    clean_tex_filename?: string;
    clean_pdf_filename?: string | null;
}

// ===== Hook Props Types =====
export interface UseFileUploadProps {
    onUploadSuccess: (data: UploadSuccessData) => void;
    onLoadingChange: (
        isLoading: boolean,
        progressValue: number,
        message?: string
    ) => void;
    selectedModel: string;
}

export interface UseCVEnhancementProps {
    onEnhanceSuccess: (data: EnhanceSuccessData) => void;
    onLoadingChange: (
        isLoading: boolean,
        progressValue: number,
        message?: string
    ) => void;
}

export interface UseModelSelectionProps {
    // No props needed - Redux manages state
}

export interface UseModelSelectionReturn {
    models: Array<{
        id: string;
        name: string;
        description: string;
        provider: string;
        default: boolean;
    }>;
    selectedModel: string;
    defaultModel: string;
    isLoading: boolean;
    error: string | null;
    setSelectedModel: (modelId: string) => void;
    refreshModels: () => Promise<void>;
}

// ===== Enhancer State Types =====
export interface EnhancerWorkflowState {
    step: "upload" | "align" | "download";
    sessionId: string | null;
}

export interface EnhancerWorkflowActions {
    setStep: (step: "upload" | "align" | "download") => void;
    setSessionId: (sessionId: string | null) => void;
    resetWorkflow: () => void;
}

export interface EnhancerJobDataState {
    jobTitle: string;
    jobDescription: string;
    companyName: string;
    inputMethod: "manual" | "file" | null;
    originalJobFile: File | null;
}

export interface EnhancerJobDataActions {
    setJobTitle: (title: string) => void;
    setJobDescription: (description: string) => void;
    setCompanyName: (name: string) => void;
    setInputMethod: (method: "manual" | "file" | null) => void;
    setOriginalJobFile: (file: File | null) => void;
    resetJobData: () => void;
}

export interface EnhancerProgressState {
    loading: boolean;
    progress: number;
    progressMessage: string;
}

export interface EnhancerProgressActions {
    setLoading: (loading: boolean) => void;
    setProgress: (progress: number) => void;
    setProgressMessage: (message: string) => void;
    handleLoadingChange: (
        isLoading: boolean,
        progressValue: number,
        message?: string
    ) => void;
    resetProgress: () => void;
}

export interface EnhancerModelConfigState {
    selectedModel: string;
    sliceProjects: boolean;
}

export interface EnhancerModelConfigActions {
    setSelectedModel: (modelId: string) => void;
    setSliceProjects: (slice: boolean) => void;
    resetModelConfig: () => void;
}

export interface EnhancerResultsState {
    generateResult: {
        tex?: string;
        pdf?: string | null;
        clean_tex_filename?: string;
        clean_pdf_filename?: string | null;
    };
}

export interface EnhancerResultsActions {
    setGenerateResult: (result: EnhancerResultsState["generateResult"]) => void;
    resetResults: () => void;
}

export interface EnhancerCVContentState {
    originalLatexContent: string;
    sections: Section[];
    originalFilename: string;
}

export interface EnhancerCVContentActions {
    setOriginalLatexContent: (content: string) => void;
    setSections: (sections: Section[]) => void;
    setOriginalFilename: (filename: string) => void;
    resetCVContent: () => void;
}

// ===== Validation Types =====
export interface ValidationRules {
    maxJobTitleLength?: number;
    maxJobDescriptionLength?: number;
    maxCompanyNameLength?: number;
    minJobTitleLength?: number;
    minJobDescriptionLength?: number;
}

export interface ValidationState {
    isValid: boolean;
    errors: {
        jobTitle?: string;
        jobDescription?: string;
        companyName?: string;
    };
    warnings: {
        jobTitle?: string;
        jobDescription?: string;
        companyName?: string;
    };
}
