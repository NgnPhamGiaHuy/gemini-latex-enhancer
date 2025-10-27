"use client";

import { setJobTitle } from "@/store/slices/jobDataSlice";
import { useAppSelector, useAppDispatch } from "@/store/hooks";

import { Input } from "@/components/ui/Input";
import { AppTooltip } from "@/components/ui/Tooltip";

interface JobTitleInputProps {
    touched: boolean;
    error?: string;
    onBlur: () => void;
}

const JobTitleInput = ({ touched, error, onBlur }: JobTitleInputProps) => {
    const dispatch = useAppDispatch();
    const jobTitle = useAppSelector((state) => state.jobData.jobTitle);

    return (
        <div className="space-y-2">
            <label className="text-sm font-medium">Job Title *</label>
            <AppTooltip content="Enter the exact title from the job posting to tailor your CV.">
                <Input
                    placeholder="e.g., Senior Software Engineer"
                    value={jobTitle}
                    onChange={(e) => dispatch(setJobTitle(e.target.value))}
                    onBlur={onBlur}
                    className="h-11"
                />
            </AppTooltip>
            {touched && error && (
                <p className="text-sm text-red-500">{error}</p>
            )}
        </div>
    );
};

export default JobTitleInput;
