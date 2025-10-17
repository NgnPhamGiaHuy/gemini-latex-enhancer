// Global/shared app types

// App step flow
export type Step = "upload" | "align" | "download";

// Hooks: useCVEnhancer
export interface CVEnhancerState {
    step: Step;
    sessionId: string | null;
    summary: string;
    sections: import("@/lib/api").Section[];
    originalLatexContent: string;
    jobTitle: string;
    jobDescription: string;
    companyName: string;
    sliceProjects: boolean;
    selectedModel: string;
    generateResult: {
        tex?: string;
        pdf?: string | null;
    };
    loading: boolean;
    progress: number;
    progressMessage: string;
    isClient: boolean;
}

export interface CVEnhancerActions {
    setStep: (step: Step) => void;
    setSessionId: (sessionId: string | null) => void;
    setSummary: (summary: string) => void;
    setSections: (sections: import("@/lib/api").Section[]) => void;
    setOriginalLatexContent: (content: string) => void;
    setJobTitle: (title: string) => void;
    setJobDescription: (description: string) => void;
    setCompanyName: (name: string) => void;
    setSliceProjects: (sliceProjects: boolean) => void;
    setSelectedModel: (modelId: string) => void;
    setGenerateResult: (result: { tex?: string; pdf?: string | null }) => void;
    setLoading: (loading: boolean) => void;
    setProgress: (progress: number) => void;
    setProgressMessage: (message: string) => void;
    handleLoadingChange: (loading: boolean, progress: number, message?: string) => void;
    resetForNewJob: () => void;
    resetState: () => void;
}

// Hooks: useCVEnhancement
export interface EnhancementParams {
    sessionId: string;
    jobTitle: string;
    jobDescription: string;
    companyName: string;
    originalLatexContent: string;
    modelId?: string;
    sliceProjects?: boolean;
}

export interface UseCVEnhancementProps {
    onEnhanceSuccess: (result: { tex?: string; pdf?: string | null }) => void;
    onLoadingChange: (loading: boolean, progress: number, message?: string) => void;
}

// Hooks: useFormValidation
export interface ValidationRules {
    maxJobTitleLength: number;
    maxJobDescriptionLength: number;
    maxCompanyNameLength: number;
    minJobTitleLength: number;
    minJobDescriptionLength: number;
}

export interface ValidationState {
    isValid: boolean;
    errors: {
        jobTitle?: string;
        jobDescription?: string;
        companyName?: string;
    };
    warnings: {
        jobDescription?: string;
    };
}

export interface UseFormValidationProps {
    jobTitle: string;
    jobDescription: string;
    companyName: string;
    rules?: Partial<ValidationRules>;
}

// Hooks: useProgressTracking
export interface ProgressState {
    loading: boolean;
    progress: number;
    message: string;
}

export interface ProgressActions {
    setLoading: (loading: boolean) => void;
    setProgress: (progress: number) => void;
    setMessage: (message: string) => void;
    updateProgress: (loading: boolean, progress: number, message?: string) => void;
    resetProgress: () => void;
}

// Hooks: useModelSelection
export interface UseModelSelectionProps {
    onModelChange?: (modelId: string) => void;
}

export interface UseModelSelectionReturn {
    models: import("@/lib/api").AIModel[];
    selectedModel: string;
    defaultModel: string;
    isLoading: boolean;
    error: string | null;
    setSelectedModel: (modelId: string) => void;
    refreshModels: () => Promise<void>;
}

// Hooks: useJobDetails
export interface JobDetailsState {
    jobTitle: string;
    jobDescription: string;
    companyName: string;
}

export interface JobDetailsActions {
    setJobTitle: (title: string) => void;
    setJobDescription: (description: string) => void;
    setCompanyName: (name: string) => void;
    resetJobDetails: () => void;
    isFormValid: boolean;
    getJobDetails: () => JobDetailsState;
}

// Hooks: useFileUpload
export interface UploadData {
    sessionId: string;
    summary: string;
    sections: import("@/lib/api").Section[];
    latexContent: string;
}

export interface UseFileUploadProps {
    onUploadSuccess: (data: UploadData) => void;
    onLoadingChange: (loading: boolean, progress: number, message?: string) => void;
    selectedModel?: string;
}

// Hooks: useAIAnalysis
export interface FormattedAnalysis {
    sections: Array<{
        title: string;
        content: string;
        isHeader: boolean;
    }>;
    hasContent: boolean;
}

// Component prop types (moved from components/types)
export interface JobDetailsFormProps {
    jobTitle: string;
    setJobTitle: (value: string) => void;
    jobDescription: string;
    setJobDescription: (value: string) => void;
    companyName: string;
    setCompanyName: (value: string) => void;
    sliceProjects: boolean;
    setSliceProjects: (value: boolean) => void;
    onBatchEnhance?: (params: { csvFile: File }) => void;
    onEnhance: () => void;
    loading: boolean;
}

export interface AlignStepProps {
    step: string;
    summary: string;
    jobTitle: string;
    setJobTitle: (value: string) => void;
    jobDescription: string;
    setJobDescription: (value: string) => void;
    companyName: string;
    setCompanyName: (value: string) => void;
    sliceProjects: boolean;
    setSliceProjects: (value: boolean) => void;
    selectedModel: string;
    onEnhanceSuccess: (result: { tex?: string; pdf?: string | null }) => void;
    onLoadingChange: (loading: boolean, progress: number, message?: string) => void;
    sessionId: string | null;
    originalLatexContent: string;
}

export interface DownloadStepProps {
    step: string;
    generateResult: {
        tex?: string;
        pdf?: string | null;
    };
    onStartOver: () => void;
    onStartAgain?: () => void;
    onBackToJobDetails?: () => void;
}

export interface UploadStepProps {
    step: string;
    selectedModel: string;
    onUploadSuccess: (data: { sessionId: string; summary: string; sections: import("@/lib/api").Section[]; latexContent: string }) => void;
    onLoadingChange: (loading: boolean, progress: number, message?: string) => void;
    onModelChange: (modelId: string) => void;
}

export interface ModelSelectionProps {
    models: import("@/lib/api").AIModel[];
    selectedModel: string;
    defaultModel: string;
    isLoading: boolean;
    error: string | null;
    onModelChange: (modelId: string) => void;
    className?: string;
}

export interface AIAnalysisProps {
    summary: string;
    loading: boolean;
}

export interface StepMeta {
    id: string;
    title: string;
    description: string;
}

export interface StepIndicatorProps {
    steps: readonly StepMeta[];
    currentStep: string;
    className?: string;
}

export interface FileUploadZoneProps {
    onDrop: (files: File[]) => void;
    isLoading: boolean;
    className?: string;
    accept?: string;
    title?: string;
    description?: string;
    processingText?: string;
}

export interface FullScreenProgressProps {
    loading: boolean;
    progress: number;
    message?: string;
    title?: string;
    subtitle?: string;
}

export type FullScreenProgressMinimalProps = Omit<FullScreenProgressProps, "title" | "subtitle">;

export interface LoadingSpinnerProps {
    size?: "sm" | "md" | "lg";
    className?: string;
}

export interface LoadingButtonProps {
    isLoading: boolean;
    children: React.ReactNode;
    className?: string;
    disabled?: boolean;
    onClick?: () => void;
}

export interface LoadingCardProps {
    isLoading: boolean;
    children: React.ReactNode;
    className?: string;
}
