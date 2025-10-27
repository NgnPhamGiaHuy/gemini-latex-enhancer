"use client";

import React from "react";
import { motion } from "framer-motion";
import { ChevronDown, Settings } from "lucide-react";

import type { AIModel } from "@/libs/api";

import { Badge } from "@/components/ui/Badge";
import { CardHeader, CardTitle } from "@/components/ui/Card";

interface ModelSelectionHeaderProps {
    models: AIModel[];
    selectedModelData: AIModel | undefined;
    isExpanded: boolean;
    setIsExpanded: (value: boolean) => void;
}

const ModelSelectionHeader: React.FC<ModelSelectionHeaderProps> = ({
    models,
    selectedModelData,
    isExpanded,
    setIsExpanded,
}) => {
    return (
        <CardHeader
            className="pb-3 cursor-pointer select-none"
            onClick={() => setIsExpanded(!isExpanded)}
        >
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Settings className="size-5 text-primary" />
                    <CardTitle className="text-base sm:text-lg lg:text-xl">
                        AI Model
                    </CardTitle>
                    <Badge variant="outline" className="text-xs">
                        {selectedModelData?.name || "Default"}
                    </Badge>
                </div>
                <motion.div
                    animate={{ rotate: isExpanded ? 180 : 0 }}
                    transition={{ duration: 0.2, ease: "easeInOut" }}
                >
                    <ChevronDown className="size-5 text-muted-foreground" />
                </motion.div>
            </div>

            {/* Selected Model Summary */}
            <div className="text-sm text-muted-foreground">
                {selectedModelData ? (
                    <span>{selectedModelData.description}</span>
                ) : (
                    <span>Choose from {models.length} available AI models</span>
                )}
            </div>
        </CardHeader>
    );
};

export default ModelSelectionHeader;
