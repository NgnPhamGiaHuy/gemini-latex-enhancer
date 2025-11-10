"use client";

import { Textarea } from "@/components/ui/Textarea";
import { AppTooltip } from "@/components/ui/Tooltip";
import { setJobDescription } from "@/store/slices/jobDataSlice";
import { useAppSelector, useAppDispatch } from "@/store/hooks";

interface JobDescriptionTextareaProps {
    touched: boolean;
    error?: string;
    warning?: string;
    onBlur: () => void;
}

const JobDescriptionTextarea = ({
    touched,
    error,
    warning,
    onBlur,
}: JobDescriptionTextareaProps) => {
    const dispatch = useAppDispatch();
    const jobDescription = useAppSelector(
        (state) => state.jobData.jobDescription
    );

    return (
        <div className="space-y-2">
            <label className="text-sm font-medium">Job Description *</label>
            <AppTooltip content="Paste the full description. The AI extracts keywords, skills, and responsibilities.">
                <Textarea
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) =>
                        dispatch(setJobDescription(e.target.value))
                    }
                    onBlur={onBlur}
                    className="h-28 sm:h-36 resize-none overflow-y-auto"
                />
            </AppTooltip>
            <div className="flex justify-between text-xs text-muted-foreground">
                <span>
                    {jobDescription.length > 15000 ? (
                        <span className="text-red-500">
                            {jobDescription.length} characters (max 15000)
                        </span>
                    ) : warning ? (
                        <span className="text-yellow-500">
                            {jobDescription.length} characters - {warning}
                        </span>
                    ) : (
                        <span>{jobDescription.length} characters</span>
                    )}
                </span>
                <span>Max 15000 characters</span>
            </div>
            {touched && error && (
                <p className="text-sm text-red-500">{error}</p>
            )}
        </div>
    );
};

export default JobDescriptionTextarea;
