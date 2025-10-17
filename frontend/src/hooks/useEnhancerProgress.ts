import { useState, useCallback } from "react";

import type { EnhancerProgressState, EnhancerProgressActions } from "@/types";

const useEnhancerProgress = (): EnhancerProgressState & EnhancerProgressActions => {
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [progressMessage, setProgressMessage] = useState("");

    const handleLoadingChange = useCallback((isLoading: boolean, progressValue: number, message: string = "") => {
        setLoading(isLoading);
        setProgress(progressValue);
        setProgressMessage(message);
    }, []);

    const resetProgress = () => {
        setLoading(false);
        setProgress(0);
        setProgressMessage("");
    };

    return {
        loading,
        progress,
        progressMessage,
        setLoading,
        setProgress,
        setProgressMessage,
        handleLoadingChange,
        resetProgress,
    };
};

export default useEnhancerProgress;
