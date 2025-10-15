import { useState, useCallback } from "react";

import type { JobDetailsState, JobDetailsActions } from "@/types";

const useJobDetails = (): JobDetailsState & JobDetailsActions => {
    const [jobTitle, setJobTitle] = useState("");
    const [jobDescription, setJobDescription] = useState("");
    const [companyName, setCompanyName] = useState("");

    const resetJobDetails = useCallback(() => {
        setJobTitle("");
        setJobDescription("");
        setCompanyName("");
    }, []);

    const isFormValid = jobTitle.trim() !== "" && jobDescription.trim() !== "" && jobDescription.length <= 15000;

    const getJobDetails = useCallback(
        () => ({
            jobTitle,
            jobDescription,
            companyName,
        }),
        [jobTitle, jobDescription, companyName]
    );

    return {
        // State
        jobTitle,
        jobDescription,
        companyName,
        // Actions
        setJobTitle,
        setJobDescription,
        setCompanyName,
        resetJobDetails,
        isFormValid,
        getJobDetails,
    };
};

export default useJobDetails;
