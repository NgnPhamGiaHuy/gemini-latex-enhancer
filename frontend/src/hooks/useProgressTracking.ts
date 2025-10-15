import { useState, useCallback } from "react";

import type { ProgressState, ProgressActions } from "@/types";

const useProgressTracking = (): ProgressState & ProgressActions => {
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [message, setMessage] = useState("");

    const updateProgress = useCallback((isLoading: boolean, progressValue: number, progressMessage: string = "") => {
        setLoading(isLoading);
        setProgress(progressValue);
        setMessage(progressMessage);
    }, []);

    const resetProgress = useCallback(() => {
        setLoading(false);
        setProgress(0);
        setMessage("");
    }, []);

    return {
        // State
        loading,
        progress,
        message,
        // Actions
        setLoading,
        setProgress,
        setMessage,
        updateProgress,
        resetProgress,
    };
};

export default useProgressTracking;
