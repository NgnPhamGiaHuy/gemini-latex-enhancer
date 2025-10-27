"use client";

import { Sparkles } from "lucide-react";
import { useDispatch } from "react-redux";

import { useBatchEnhancement, useJobFileUpload } from "@/hooks";

import { getFileUploadDescription } from "@/utils";
import { handleLoadingChange } from "@/store/slices/progressSlice";

import { LoadingButton } from "@/components/ui/LoadingButton";
import { FileUploadZone } from "@/components/ui/FileUploadZone";
import SliceProjectsCheckbox from "@/components/features/job-details/SliceProjectsCheckbox";

interface JobFileUploadSectionProps {
    loading: boolean;
}

const JobFileUploadSection = ({ loading }: JobFileUploadSectionProps) => {
    const dispatch = useDispatch();

    const {
        jobFile,
        fileError,
        filePreview,
        handleFileRemove,
        handleFileUpload,
    } = useJobFileUpload();

    const { handleBatchEnhance } = useBatchEnhancement({
        onLoadingChange: (isLoading, progressValue, message = "") => {
            dispatch(
                handleLoadingChange({ isLoading, progressValue, message })
            );
        },
    });

    return (
        <div className="space-y-4">
            <div className="space-y-2">
                {!filePreview.length && (
                    <FileUploadZone
                        onDrop={handleFileUpload}
                        isLoading={false}
                        accept=".csv,.json"
                        title="Upload your job file"
                        description={getFileUploadDescription()}
                        processingText="Reading file..."
                    />
                )}

                {fileError && (
                    <p className="text-sm text-red-500">{fileError}</p>
                )}

                {filePreview.length > 0 && jobFile && (
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <div className="text-xs text-muted-foreground">
                                <p>
                                    Valid file detected. Preview (first 3
                                    entries):
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
                            {filePreview.slice(1, 4).map((row, idx) => (
                                <div
                                    className="grid grid-cols-3 gap-2 p-2 border-t"
                                    key={idx}
                                >
                                    {row.slice(0, 3).map((c, i) => (
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

            <SliceProjectsCheckbox
                id="slice-projects-batch"
                showDescription={false}
            />

            <LoadingButton
                isLoading={loading}
                onClick={() =>
                    jobFile &&
                    handleBatchEnhance &&
                    handleBatchEnhance({ jobFile })
                }
                disabled={!jobFile || !!fileError}
                className="w-full h-11"
            >
                <Sparkles className="h-4 w-4" />
                Start Batch Enhancement
            </LoadingButton>
        </div>
    );
};

export default JobFileUploadSection;
