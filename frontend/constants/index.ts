type Step = "upload" | "align" | "download";

export const DEFAULT_MODEL = "gemini-2.5-flash";

export const STEPS = [
    { id: "upload", title: "Upload CV", description: "Upload your LaTeX CV" },
    { id: "align", title: "Job Details", description: "Enter target job info" },
    { id: "download", title: "Download", description: "Get your tailored CV" },
] as const satisfies readonly {
    id: Step;
    title: string;
    description: string;
}[];

export const MODEL_PATTERNS = {
    badge: {
        pro: "secondary",
        preview: "outline",
        exp: "outline",
        default: "default",
    },
    description: {
        preview: "Preview",
        exp: "Experimental",
        lite: "Lightweight",
        pro: "Advanced",
    },
    category: {
        "2.5": "2.5 Series",
        "2.0": "2.0 Series",
        "1.5": "1.5 Series",
        "1.0": "1.0 Series",
        gemma: "Gemma Series",
    },
} as const;
