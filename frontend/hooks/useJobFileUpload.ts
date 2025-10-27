import { useState } from "react";

import { previewFile } from "@/libs/api";

interface UseJobFileUploadReturn {
    jobFile: File | null;
    fileError: string;
    filePreview: string[][];
    handleFileRemove: () => void;
    handleFileUpload: (files: File[]) => Promise<void>;
}

const useJobFileUpload = (): UseJobFileUploadReturn => {
    const [jobFile, setJobFile] = useState<File | null>(null);
    const [fileError, setFileError] = useState<string>("");
    const [filePreview, setFilePreview] = useState<string[][]>([]);

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

    return {
        jobFile,
        fileError,
        filePreview,
        handleFileRemove,
        handleFileUpload,
    };
};

export default useJobFileUpload;
