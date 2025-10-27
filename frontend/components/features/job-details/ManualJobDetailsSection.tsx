"use client";

import { Sparkles } from "lucide-react";

import { useResumeEnhancement } from "@/hooks";

import { useAppDispatch } from "@/store/hooks";
import { setStep } from "@/store/slices/workflowSlice";
import { setInputMethod } from "@/store/slices/jobDataSlice";
import { setGenerateResult } from "@/store/slices/resultsSlice";
import { handleLoadingChange } from "@/store/slices/progressSlice";

import { LoadingButton } from "@/components/ui/LoadingButton";
import JobTitleInput from "@/components/features/job-details/JobTitleInput";
import CompanyNameInput from "@/components/features/job-details/CompanyNameInput";
import SliceProjectsCheckbox from "@/components/features/job-details/SliceProjectsCheckbox";
import JobDescriptionTextarea from "@/components/features/job-details/JobDescriptionTextarea";

interface ManualJobDetailsSectionProps {
    loading: boolean;
    touchedFields: {
        jobTitle: boolean;
        jobDescription: boolean;
        companyName: boolean;
    };
    errors: {
        jobTitle?: string;
        jobDescription?: string;
        companyName?: string;
    };
    warnings: {
        jobDescription?: string;
    };
    isValid: boolean;
    handleFieldBlur: (fieldName: string) => void;
}

const ManualJobDetailsSection = ({
    loading,
    touchedFields,
    errors,
    warnings,
    isValid,
    handleFieldBlur,
}: ManualJobDetailsSectionProps) => {
    const dispatch = useAppDispatch();

    const handleEnhancement = useResumeEnhancement({
        onEnhanceSuccess: (result) => {
            dispatch(setGenerateResult(result));
            dispatch(setStep("download"));
            dispatch(setInputMethod("manual"));
        },
        onLoadingChange: (isLoading, progressValue, message = "") => {
            dispatch(
                handleLoadingChange({ isLoading, progressValue, message })
            );
        },
    });

    return (
        <div className="space-y-4">
            <JobTitleInput
                touched={touchedFields.jobTitle}
                error={errors.jobTitle}
                onBlur={() => handleFieldBlur("jobTitle")}
            />

            <CompanyNameInput
                touched={touchedFields.companyName}
                error={errors.companyName}
                onBlur={() => handleFieldBlur("companyName")}
            />

            <JobDescriptionTextarea
                touched={touchedFields.jobDescription}
                error={errors.jobDescription}
                warning={warnings.jobDescription}
                onBlur={() => handleFieldBlur("jobDescription")}
            />

            <SliceProjectsCheckbox />

            <LoadingButton
                isLoading={loading}
                onClick={handleEnhancement}
                disabled={!isValid}
                className="w-full h-11"
            >
                <Sparkles className="h-4 w-4" />
                Optimize CV with AI
            </LoadingButton>
        </div>
    );
};

export default ManualJobDetailsSection;
