import React, { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import type { AIModel } from "@/libs/api";

import { CardContent } from "@/components/ui/Card";
import ModelHelpText from "@/components/features/model-selection/ModelHelpText";
import SearchModelInput from "@/components/features/model-selection/SearchModelInput";
import SelectedModelInfo from "@/components/features/model-selection/SelectedModelInfo";
import ModelSelectDropdown from "@/components/features/model-selection/ModelSelectDropdown";

interface ModelSelectionCollapsibleProps {
    models: AIModel[];
    selectedModelData: AIModel | undefined;
    isExpanded: boolean;
}

const ModelSelectionCollapsible: React.FC<ModelSelectionCollapsibleProps> = ({
    models,
    selectedModelData,
    isExpanded,
}) => {
    const [searchTerm, setSearchTerm] = useState<string>("");

    return (
        <AnimatePresence>
            {isExpanded && (
                <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{
                        duration: 0.3,
                        ease: "easeInOut",
                        opacity: { duration: 0.2 },
                    }}
                    className="overflow-hidden"
                >
                    <CardContent className="pt-0 space-y-4">
                        <SearchModelInput
                            searchTerm={searchTerm}
                            onSearchChange={setSearchTerm}
                        />

                        <ModelSelectDropdown
                            models={models}
                            searchTerm={searchTerm}
                        />

                        {selectedModelData && (
                            <SelectedModelInfo model={selectedModelData} />
                        )}

                        <ModelHelpText />
                    </CardContent>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default ModelSelectionCollapsible;
