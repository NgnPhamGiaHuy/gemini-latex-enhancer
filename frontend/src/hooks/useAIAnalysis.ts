import { useMemo } from "react";

import type { FormattedAnalysis } from "@/types";

const useAIAnalysis = (summary: string): FormattedAnalysis => {
    const formattedAnalysis = useMemo(() => {
        if (!summary) {
            return {
                sections: [],
                hasContent: false,
            };
        }

        const parts = summary.split(/\*\*(.*?)\*\*/);
        const sections = parts
            .map((part, index) => {
                if (index % 2 === 1) {
                    return {
                        title: part.replace(/:\s*$/, ""),
                        content: "",
                        isHeader: true,
                    };
                } else if (part.trim()) {
                    const cleanText = part.replace(/^:\s*/, "").trim();
                    if (cleanText) {
                        return {
                            title: "",
                            content: cleanText,
                            isHeader: false,
                        };
                    }
                }
                return null;
            })
            .filter((item): item is { title: string; content: string; isHeader: boolean } => item !== null);

        return {
            sections,
            hasContent: sections.length > 0,
        };
    }, [summary]);

    return formattedAnalysis;
};

export default useAIAnalysis;
