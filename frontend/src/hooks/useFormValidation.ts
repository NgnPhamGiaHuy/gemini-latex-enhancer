import { useMemo } from "react";

import type { ValidationRules, ValidationState, UseFormValidationProps } from "@/types";

const DEFAULT_RULES: ValidationRules = {
    maxJobTitleLength: 200,
    maxJobDescriptionLength: 15000,
    maxCompanyNameLength: 100,
    minJobTitleLength: 1,
    minJobDescriptionLength: 10,
};

const useFormValidation = ({ jobTitle, jobDescription, companyName, rules = {} }: UseFormValidationProps): ValidationState => {
    const validationState = useMemo(() => {
        const validationRules = { ...DEFAULT_RULES, ...rules };
        const errors: ValidationState["errors"] = {};
        const warnings: ValidationState["warnings"] = {};

        // Job Title validation
        if (!jobTitle.trim()) {
            errors.jobTitle = "Job title is required";
        } else if (jobTitle.length < validationRules.minJobTitleLength) {
            errors.jobTitle = `Job title must be at least ${validationRules.minJobTitleLength} characters`;
        } else if (jobTitle.length > validationRules.maxJobTitleLength) {
            errors.jobTitle = `Job title must be less than ${validationRules.maxJobTitleLength} characters`;
        }

        // Job Description validation
        if (!jobDescription.trim()) {
            errors.jobDescription = "Job description is required";
        } else if (jobDescription.length < validationRules.minJobDescriptionLength) {
            errors.jobDescription = `Job description must be at least ${validationRules.minJobDescriptionLength} characters`;
        } else if (jobDescription.length > validationRules.maxJobDescriptionLength) {
            errors.jobDescription = `Job description must be less than ${validationRules.maxJobDescriptionLength} characters`;
        }

        // Always show warnings (they're helpful, not errors)
        if (jobDescription.length > validationRules.maxJobDescriptionLength * 0.9) {
            warnings.jobDescription = "Job description is approaching the character limit";
        }

        // Company Name validation (optional)
        if (companyName && companyName.length > validationRules.maxCompanyNameLength) {
            errors.companyName = `Company name must be less than ${validationRules.maxCompanyNameLength} characters`;
        }

        const isValid = Object.keys(errors).length === 0;

        return {
            isValid,
            errors,
            warnings,
        };
    }, [jobTitle, jobDescription, companyName, rules]);

    return validationState;
};

export default useFormValidation;
