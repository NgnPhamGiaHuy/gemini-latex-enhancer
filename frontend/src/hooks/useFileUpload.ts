import { toast } from "sonner";
import { useCallback } from "react";

import type { UseFileUploadProps } from "@/types";

import { uploadTex } from "@/lib/api";

const useFileUpload = ({
    onUploadSuccess,
    onLoadingChange,
    selectedModel,
}: UseFileUploadProps) => {
    const handleFileUpload = useCallback(
        async (acceptedFiles: File[]) => {
            if (!acceptedFiles.length) return;

            onLoadingChange(true, 10, "Uploading CV file...");

            try {
                onLoadingChange(true, 30, "Processing LaTeX content...");

                const res = await uploadTex(acceptedFiles[0], selectedModel);

                onLoadingChange(true, 60, "Generating AI analysis...");

                const fileContent = await acceptedFiles[0].text();

                onLoadingChange(true, 90, "Finalizing analysis...");

                onUploadSuccess({
                    sessionId: res.session_id,
                    sections: res.sections,
                    latexContent: fileContent,
                    originalFilename: res.original_filename,
                });

                onLoadingChange(false, 100, "Upload completed!");
                toast.success("CV uploaded and analyzed successfully!");
            } catch (error) {
                console.error("Upload failed:", error);
                onLoadingChange(false, 0, "Upload failed");
                toast.error("Failed to upload CV. Please try again.");
            }
        },
        [onUploadSuccess, onLoadingChange, selectedModel]
    );

    return {
        handleFileUpload,
    };
};

export default useFileUpload;
