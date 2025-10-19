import { useState } from "react";

import type { Section } from "@/lib/api";
import type { EnhancerCVContentState, EnhancerCVContentActions } from "@/types";

const useEnhancerCVContent = (): EnhancerCVContentState &
    EnhancerCVContentActions => {
    const [originalLatexContent, setOriginalLatexContent] =
        useState<string>("");
    const [sections, setSections] = useState<Section[]>([]);

    const resetCVContent = () => {
        setOriginalLatexContent("");
        setSections([]);
    };

    return {
        originalLatexContent,
        sections,
        setOriginalLatexContent,
        setSections,
        resetCVContent,
    };
};

export default useEnhancerCVContent;
