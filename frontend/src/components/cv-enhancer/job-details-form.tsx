"use client";

import { useState } from "react";
import { Target, Sparkles, Scissors } from "lucide-react";

import type { JobDetailsFormProps } from "@/types";

import { previewFile } from "@/lib/api";
import { useFormValidation } from "@/hooks";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { AppTooltip } from "@/components/ui/tooltip";
import { LoadingButton } from "@/components/ui/loading";
import { FileUploadZone } from "@/components/ui/file-upload";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const JobDetailsForm = ({
    jobTitle,
    setJobTitle,
    jobDescription,
    setJobDescription,
    companyName,
    setCompanyName,
    sliceProjects,
    setSliceProjects,
    onEnhance,
    onBatchEnhance,
    loading,
}: JobDetailsFormProps) => {
    const [mode, setMode] = useState<"manual" | "file">("manual");
    const [jobFile, setJobFile] = useState<File | null>(null);
    const [fileError, setFileError] = useState<string>("");
    const [filePreview, setFilePreview] = useState<string[][]>([]);
    const [touchedFields, setTouchedFields] = useState({
        jobTitle: false,
        jobDescription: false,
        companyName: false,
    });

    const { isValid, errors, warnings } = useFormValidation({
        jobTitle,
        jobDescription,
        companyName,
    });

    const handleFieldBlur = (fieldName: keyof typeof touchedFields) => {
        setTouchedFields((prev) => ({ ...prev, [fieldName]: true }));
    };

    const handleFileRemove = () => {
        setJobFile(null);
        setFilePreview([]);
        setFileError("");
    };

    const handleFileUpload = async (files: File[]) => {
        const file = files[0];
        if (!file) return;

        // Validate file type
        const fileExtension = file.name.toLowerCase().split(".").pop();
        if (!["csv", "json"].includes(fileExtension || "")) {
            setFileError("Please upload a CSV or JSON file.");
            return;
        }

        setJobFile(file);
        setFilePreview([]);
        setFileError("");

        try {
            const preview = await previewFile(file);
            const headersLower = preview.headers.map((h) => h.toLowerCase());

            // Check for required fields with flexible matching
            const hasTitle = headersLower.some(
                (h) =>
                    h.includes("title") ||
                    h.includes("position") ||
                    h.includes("role") ||
                    h.includes("job")
            );
            const hasDesc = headersLower.some(
                (h) =>
                    h.includes("description") ||
                    h.includes("desc") ||
                    h.includes("responsibilities") ||
                    h.includes("duties")
            );

            if (!hasTitle || !hasDesc) {
                setFileError(
                    "File must include Job Title and Job Description fields (or their variations)."
                );
                return;
            }

            setFilePreview([preview.headers, ...preview.rows]);
        } catch {
            setFileError("Failed to preview file");
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5 text-primary" />
                    Target Job Details
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <Tabs
                    value={mode}
                    onValueChange={(v: string) =>
                        setMode(v as "manual" | "file")
                    }
                >
                    <TabsList className="grid grid-cols-2 w-full">
                        <TabsTrigger value="manual">Manual Input</TabsTrigger>
                        <TabsTrigger value="file">File Upload</TabsTrigger>
                    </TabsList>

                    <TabsContent value="manual" className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">
                                Job Title *
                            </label>
                            <AppTooltip content="Enter the exact title from the job posting to tailor your CV.">
                                <Input
                                    placeholder="e.g., Senior Software Engineer"
                                    value={jobTitle}
                                    onChange={(e) =>
                                        setJobTitle(e.target.value)
                                    }
                                    onBlur={() => handleFieldBlur("jobTitle")}
                                    className="h-11"
                                />
                            </AppTooltip>
                            {touchedFields.jobTitle && errors.jobTitle && (
                                <p className="text-sm text-red-500">
                                    {errors.jobTitle}
                                </p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">
                                Company Name
                            </label>
                            <AppTooltip content="Optional. Improves tone and relevance if provided.">
                                <Input
                                    placeholder="e.g., Google, Microsoft"
                                    value={companyName}
                                    onChange={(e) =>
                                        setCompanyName(e.target.value)
                                    }
                                    onBlur={() =>
                                        handleFieldBlur("companyName")
                                    }
                                    className="h-11"
                                />
                            </AppTooltip>
                            {touchedFields.companyName &&
                                errors.companyName && (
                                    <p className="text-sm text-red-500">
                                        {errors.companyName}
                                    </p>
                                )}
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">
                                Job Description *
                            </label>
                            <AppTooltip content="Paste the full description. The AI extracts keywords, skills, and responsibilities.">
                                <Textarea
                                    placeholder="Paste the job description here..."
                                    value={jobDescription}
                                    onChange={(e) =>
                                        setJobDescription(e.target.value)
                                    }
                                    onBlur={() =>
                                        handleFieldBlur("jobDescription")
                                    }
                                    className="resize-none h-32 sm:h-40 overflow-y-auto"
                                />
                            </AppTooltip>
                            <div className="flex justify-between text-xs text-muted-foreground">
                                <span>
                                    {jobDescription.length > 15000 ? (
                                        <span className="text-red-500">
                                            {jobDescription.length} characters
                                            (max 15000)
                                        </span>
                                    ) : warnings.jobDescription ? (
                                        <span className="text-yellow-500">
                                            {jobDescription.length} characters -{" "}
                                            {warnings.jobDescription}
                                        </span>
                                    ) : (
                                        <span>
                                            {jobDescription.length} characters
                                        </span>
                                    )}
                                </span>
                                <span>Max 15000 characters</span>
                            </div>
                            {touchedFields.jobDescription &&
                                errors.jobDescription && (
                                    <p className="text-sm text-red-500">
                                        {errors.jobDescription}
                                    </p>
                                )}
                        </div>

                        <div className="space-y-3">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="slice-projects"
                                    checked={sliceProjects}
                                    onCheckedChange={(checked: boolean) =>
                                        setSliceProjects(checked)
                                    }
                                />
                                <label
                                    htmlFor="slice-projects"
                                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer flex items-center gap-2"
                                >
                                    <Scissors className="h-4 w-4 text-primary" />
                                    Slice personal projects to fit one page
                                </label>
                            </div>
                            <AppTooltip content="Keeps the CV concise by limiting projects to the most relevant ones.">
                                <p className="text-xs text-muted-foreground ml-6">
                                    When enabled, AI will intelligently select
                                    only the most job-relevant projects (2-3
                                    projects max) to ensure your CV fits on one
                                    page.
                                </p>
                            </AppTooltip>
                        </div>

                        <LoadingButton
                            isLoading={loading}
                            onClick={onEnhance}
                            disabled={!isValid}
                            className="w-full h-11"
                        >
                            <Sparkles className="h-4 w-4" />
                            Optimize CV with AI
                        </LoadingButton>
                    </TabsContent>

                    <TabsContent value="file" className="space-y-4">
                        <div className="space-y-2">
                            {!filePreview.length && (
                                <FileUploadZone
                                    onDrop={handleFileUpload}
                                    isLoading={false}
                                    accept=".csv,.json"
                                    title="Upload your job file"
                                    description={
                                        (
                                            <>
                                                Drag and drop your{" "}
                                                <code className="px-1 py-0.5 bg-white nb-border text-xs">
                                                    .csv
                                                </code>{" "}
                                                or{" "}
                                                <code className="px-1 py-0.5 bg-white nb-border text-xs">
                                                    .json
                                                </code>{" "}
                                                file here, or click to browse
                                            </>
                                        ) as unknown as string
                                    }
                                    processingText="Reading file..."
                                />
                            )}

                            {fileError && (
                                <p className="text-sm text-red-500">
                                    {fileError}
                                </p>
                            )}

                            {filePreview.length > 0 && jobFile && (
                                <div className="space-y-3">
                                    <div className="flex items-center justify-between">
                                        <div className="text-xs text-muted-foreground">
                                            <p>
                                                Valid file detected. Preview
                                                (first 3 entries):
                                            </p>
                                            <p className="text-[11px] text-muted-foreground">
                                                {jobFile.name}
                                            </p>
                                        </div>
                                        <button
                                            onClick={handleFileRemove}
                                            className="text-red-500 hover:text-red-700 text-sm font-medium"
                                            type="button"
                                        >
                                            × Remove
                                        </button>
                                    </div>
                                    <div className="nb-border nb-shadow bg-white overflow-hidden">
                                        <div className="grid grid-cols-3 gap-2 p-2 font-bold bg-accent text-accent-foreground">
                                            {(filePreview[0] || [])
                                                .slice(0, 3)
                                                .map((h, i) => (
                                                    <div key={i}>{h}</div>
                                                ))}
                                        </div>
                                        {filePreview
                                            .slice(1, 4)
                                            .map((row, idx) => (
                                                <div
                                                    className="grid grid-cols-3 gap-2 p-2 border-t"
                                                    key={idx}
                                                >
                                                    {row
                                                        .slice(0, 3)
                                                        .map((c, i) => (
                                                            <div
                                                                key={i}
                                                                className="truncate"
                                                                title={c}
                                                            >
                                                                {c}
                                                            </div>
                                                        ))}
                                                </div>
                                            ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="space-y-3">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="slice-projects-batch"
                                    checked={sliceProjects}
                                    onCheckedChange={(checked: boolean) =>
                                        setSliceProjects(checked)
                                    }
                                />
                                <label
                                    htmlFor="slice-projects-batch"
                                    className="text-sm font-medium leading-none cursor-pointer flex items-center gap-2"
                                >
                                    <Scissors className="h-4 w-4 text-primary" />{" "}
                                    Apply project slicing during batch
                                </label>
                            </div>
                        </div>

                        <LoadingButton
                            isLoading={loading}
                            onClick={() =>
                                jobFile &&
                                onBatchEnhance &&
                                onBatchEnhance({ jobFile })
                            }
                            disabled={!jobFile || !!fileError}
                            className="w-full h-11"
                        >
                            <Sparkles className="h-4 w-4" />
                            Start Batch Enhancement
                        </LoadingButton>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
};

export default JobDetailsForm;
