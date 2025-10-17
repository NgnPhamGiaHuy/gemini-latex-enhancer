import { useState } from "react";

import type { Section } from "@/lib/api";
import type { EnhancerCVContentState, EnhancerCVContentActions } from "@/types";

const useEnhancerCVContent = (): EnhancerCVContentState & EnhancerCVContentActions => {
    const [originalLatexContent, setOriginalLatexContent] = useState<string>("");
    const [summary, setSummary] = useState<string>("");
    const [sections, setSections] = useState<Section[]>([]);

    const resetCVContent = () => {
        setOriginalLatexContent("");
        setSummary("");
        setSections([]);
    };

    return {
        originalLatexContent,
        summary,
        sections,
        setOriginalLatexContent,
        setSummary,
        setSections,
        resetCVContent,
    };
};

export default useEnhancerCVContent;
