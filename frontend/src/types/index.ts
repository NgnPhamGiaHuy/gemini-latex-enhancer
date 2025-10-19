// Global/shared app types
export type Step = "upload" | "align" | "download";

export interface EnhancerWorkflowState {
    step: Step;
    sessionId: string | null;
}

export interface EnhancerWorkflowActions {
    setStep: (step: Step) => void;
    setSessionId: (id: string | null) => void;
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
    setJobTitle: (value: string) => void;
    setJobDescription: (value: string) => void;
    setCompanyName: (value: string) => void;
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
    setLoading: (value: boolean) => void;
    setProgress: (value: number) => void;
    setProgressMessage: (value: string) => void;
    handleLoadingChange: (
        loading: boolean,
        progress: number,
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
    setSliceProjects: (value: boolean) => void;
    resetModelConfig: () => void;
}

export interface EnhancerResultsState {
    generateResult: {
        tex?: string;
        pdf?: string | null;
    };
}

export interface EnhancerResultsActions {
    setGenerateResult: (result: { tex?: string; pdf?: string | null }) => void;
    resetResults: () => void;
}

export interface EnhancerCVContentState {
    originalLatexContent: string;
    sections: import("@/lib/api").Section[];
}

export interface EnhancerCVContentActions {
    setOriginalLatexContent: (value: string) => void;
    setSections: (value: import("@/lib/api").Section[]) => void;
    resetCVContent: () => void;
}

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
    onLoadingChange: (
        loading: boolean,
        progress: number,
        message?: string
    ) => void;
}

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

export interface UploadData {
    sessionId: string;
    sections: import("@/lib/api").Section[];
    latexContent: string;
}

export interface UseFileUploadProps {
    onUploadSuccess: (data: UploadData) => void;
    onLoadingChange: (
        loading: boolean,
        progress: number,
        message?: string
    ) => void;
    selectedModel?: string;
}

export interface JobDetailsFormProps {
    jobTitle: string;
    setJobTitle: (value: string) => void;
    jobDescription: string;
    setJobDescription: (value: string) => void;
    companyName: string;
    setCompanyName: (value: string) => void;
    sliceProjects: boolean;
    setSliceProjects: (value: boolean) => void;
    onBatchEnhance?: (params: { jobFile: File }) => void;
    onEnhance: () => void;
    loading: boolean;
}

export interface AlignStepProps {
    step: string;
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
    onLoadingChange: (
        loading: boolean,
        progress: number,
        message?: string
    ) => void;
    sessionId: string | null;
    originalLatexContent: string;
    onBatchJobDetailsExtracted?: (jobDetails: {
        jobTitle: string;
        jobDescription: string;
        companyName: string;
    }) => void;
    onBatchEnhancementSuccess?: (
        result: { tex?: string; pdf?: string | null },
        jobFile: File
    ) => void;
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
    inputMethod?: "manual" | "file" | null;
    onRegenerateSingle?: () => void;
    onRegenerateBatch?: () => void;
}

export interface UploadStepProps {
    step: string;
    selectedModel: string;
    onUploadSuccess: (data: {
        sessionId: string;
        sections: import("@/lib/api").Section[];
        latexContent: string;
    }) => void;
    onLoadingChange: (
        loading: boolean,
        progress: number,
        message?: string
    ) => void;
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

export type FullScreenProgressMinimalProps = Omit<
    FullScreenProgressProps,
    "title" | "subtitle"
>;

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
