import { useState } from "react";

import type { Section } from "@/lib/api";
import type { EnhancerCVContentState, EnhancerCVContentActions } from "@/types";

const useEnhancerCVContent = (): EnhancerCVContentState &
    EnhancerCVContentActions => {
    const [originalLatexContent, setOriginalLatexContent] =
        useState<string>("");
    const [sections, setSections] = useState<Section[]>([]);
    const [originalFilename, setOriginalFilename] = useState<string>("");

    const resetCVContent = () => {
        setOriginalLatexContent("");
        setSections([]);
        setOriginalFilename("");
    };

    return {
        originalLatexContent,
        sections,
        originalFilename,
        setOriginalLatexContent,
        setSections,
        setOriginalFilename,
        resetCVContent,
    };
};

export default useEnhancerCVContent;
