import { useState } from "react";

import type { EnhancerResultsState, EnhancerResultsActions } from "@/types";

const useEnhancerResults = (): EnhancerResultsState &
    EnhancerResultsActions => {
    const [generateResult, setGenerateResult] = useState<{
        tex?: string;
        pdf?: string | null;
    }>({});

    const resetResults = () => setGenerateResult({});

    return { generateResult, setGenerateResult, resetResults };
};

export default useEnhancerResults;
