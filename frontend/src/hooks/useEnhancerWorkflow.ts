import { useState } from "react";

import type { Step, EnhancerWorkflowState, EnhancerWorkflowActions } from "@/types";

const useEnhancerWorkflow = (): EnhancerWorkflowState & EnhancerWorkflowActions => {
    const [step, setStep] = useState<Step>("upload");
    const [sessionId, setSessionId] = useState<string | null>(null);

    const resetWorkflow = () => {
        setStep("upload");
        setSessionId(null);
    };

    return {
        step,
        sessionId,
        setStep,
        setSessionId,
        resetWorkflow,
    };
};

export default useEnhancerWorkflow;
