import { useState } from "react";

import type { EnhancerJobDataState, EnhancerJobDataActions } from "@/types";

const useEnhancerJobData = (): EnhancerJobDataState & EnhancerJobDataActions => {
    const [jobTitle, setJobTitle] = useState("");
    const [jobDescription, setJobDescription] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [inputMethod, setInputMethod] = useState<"manual" | "file" | null>(null);
    const [originalJobFile, setOriginalJobFile] = useState<File | null>(null);

    const resetJobData = () => {
        setJobTitle("");
        setJobDescription("");
        setCompanyName("");
        setInputMethod(null);
        setOriginalJobFile(null);
    };

    return {
        jobTitle,
        jobDescription,
        companyName,
        inputMethod,
        originalJobFile,
        setJobTitle,
        setJobDescription,
        setCompanyName,
        setInputMethod,
        setOriginalJobFile,
        resetJobData,
    };
};

export default useEnhancerJobData;
