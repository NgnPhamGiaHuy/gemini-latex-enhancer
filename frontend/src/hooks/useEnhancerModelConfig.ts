import { useState } from "react";

import type {
    EnhancerModelConfigState,
    EnhancerModelConfigActions,
} from "@/types";

const DEFAULT_MODEL = "gemini-2.5-flash";

const useEnhancerModelConfig = (): EnhancerModelConfigState &
    EnhancerModelConfigActions => {
    const [selectedModel, setSelectedModel] = useState<string>(DEFAULT_MODEL);
    const [sliceProjects, setSliceProjects] = useState<boolean>(true);

    const resetModelConfig = () => {
        setSelectedModel(DEFAULT_MODEL);
        setSliceProjects(true);
    };

    return {
        selectedModel,
        sliceProjects,
        setSelectedModel,
        setSliceProjects,
        resetModelConfig,
    };
};

export default useEnhancerModelConfig;
