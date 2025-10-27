import { useMemo } from "react";

import type { ValidationRules, ValidationState } from "@/types";

import { useAppSelector } from "@/store/hooks";

interface RequiredValidationRules {
    maxJobTitleLength: number;
    maxJobDescriptionLength: number;
    maxCompanyNameLength: number;
    minJobTitleLength: number;
    minJobDescriptionLength: number;
}

const DEFAULT_RULES: RequiredValidationRules = {
    maxJobTitleLength: 200,
    maxJobDescriptionLength: 15000,
    maxCompanyNameLength: 100,
    minJobTitleLength: 1,
    minJobDescriptionLength: 10,
};

interface UseFormValidationProps {
    rules?: Partial<ValidationRules>;
}

const useFormValidation = (
    props: UseFormValidationProps = {}
): ValidationState => {
    const { rules = {} } = props;
    const jobTitle = useAppSelector((state) => state.jobData.jobTitle);
    const jobDescription = useAppSelector(
        (state) => state.jobData.jobDescription
    );
    const companyName = useAppSelector((state) => state.jobData.companyName);

    const validationState = useMemo(() => {
        const validationRules: RequiredValidationRules = {
            ...DEFAULT_RULES,
            ...rules,
        };
        const errors: ValidationState["errors"] = {};
        const warnings: ValidationState["warnings"] = {};

        if (!jobTitle.trim()) {
            errors.jobTitle = "Job title is required";
        } else if (jobTitle.length < validationRules.minJobTitleLength) {
            errors.jobTitle = `Job title must be at least ${validationRules.minJobTitleLength} characters`;
        } else if (jobTitle.length > validationRules.maxJobTitleLength) {
            errors.jobTitle = `Job title must be less than ${validationRules.maxJobTitleLength} characters`;
        }

        if (!jobDescription.trim()) {
            errors.jobDescription = "Job description is required";
        } else if (
            jobDescription.length < validationRules.minJobDescriptionLength
        ) {
            errors.jobDescription = `Job description must be at least ${validationRules.minJobDescriptionLength} characters`;
        } else if (
            jobDescription.length > validationRules.maxJobDescriptionLength
        ) {
            errors.jobDescription = `Job description must be less than ${validationRules.maxJobDescriptionLength} characters`;
        }

        if (
            jobDescription.length >
            validationRules.maxJobDescriptionLength * 0.9
        ) {
            warnings.jobDescription =
                "Job description is approaching the character limit";
        }

        if (
            companyName &&
            companyName.length > validationRules.maxCompanyNameLength
        ) {
            errors.companyName = `Company name must be less than ${validationRules.maxCompanyNameLength} characters`;
        }

        const isValid = Object.keys(errors).length === 0;

        return {
            isValid,
            errors,
            warnings,
        };
    }, [jobTitle, jobDescription, companyName, props.rules]);

    return validationState;
};

export default useFormValidation;
