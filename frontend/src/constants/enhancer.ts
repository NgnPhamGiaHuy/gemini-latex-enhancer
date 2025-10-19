import type { Step } from "@/types";

export function getProgressTitle(message: string): string {
    if (message.includes("Preparing")) return "Preparing Enhancement";
    if (message.includes("Analyzing")) return "Analyzing Job Requirements";
    if (message.includes("Generating")) return "Generating Enhanced CV";
    if (message.includes("Compiling")) return "Compiling LaTeX to PDF";
    if (message.includes("completed")) return "Enhancement Complete!";
    if (message.includes("failed")) return "Enhancement Failed";
    return "Enhancing Your CV";
}

export function getProgressSubtitle(message: string): string {
    if (message.includes("Preparing"))
        return "Setting up AI processing pipeline...";
    if (message.includes("Analyzing"))
        return "Extracting key requirements and skills from job description...";
    if (message.includes("Generating"))
        return "AI is optimizing your CV content to match job requirements...";
    if (message.includes("Compiling"))
        return "Converting enhanced LaTeX to PDF format...";
    if (message.includes("completed")) return "Your CV is ready for download!";
    if (message.includes("failed"))
        return "Something went wrong. Please try again.";
    return "AI is analyzing and optimizing your CV to match the job requirements";
}

export const STEPS = [
    { id: "upload", title: "Upload CV", description: "Upload your LaTeX CV" },
    { id: "align", title: "Job Details", description: "Enter target job info" },
    { id: "download", title: "Download", description: "Get your tailored CV" },
] as const satisfies readonly {
    id: Step;
    title: string;
    description: string;
}[];
