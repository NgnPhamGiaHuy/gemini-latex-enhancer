"use client";

import React, { useState } from "react";

import { cn } from "@/libs/utils";
import { useAppSelector } from "@/store/hooks";

import { Card } from "@/components/ui/Card";
import ModelSelectionHeader from "@/components/features/ModelSelectionHeader";
import ModelErrorState from "@/components/features/model-selection/ModelErrorState";
import ModelLoadingState from "@/components/features/model-selection/ModelLoadingState";
import ModelSelectionCollapsible from "@/components/features/ModelSelectionCollapsible";

interface ModelSelectionProps {
    error: string | null;
    isLoading: boolean;
    className?: string;
}

const ModelSelection: React.FC<ModelSelectionProps> = ({
    error,
    isLoading,
    className,
}) => {
    const [isExpanded, setIsExpanded] = useState<boolean>(false);

    const models = useAppSelector((state) => state.modelSelection.models);
    const defaultModel = useAppSelector(
        (state) => state.modelSelection.defaultModel
    );
    const selectedModel = useAppSelector(
        (state) => state.modelSelection.selectedModel
    );

    const selectedModelData = models.find((m) => m.id === selectedModel);

    if (error) {
        return (
            <ModelErrorState
                defaultModel={defaultModel}
                className={className}
            />
        );
    }

    if (isLoading) {
        return <ModelLoadingState className={className} />;
    }

    return (
        <Card
            className={cn(
                "transition-all duration-300",
                isExpanded && "nb-shadow-lg",
                className
            )}
        >
            <ModelSelectionHeader
                models={models}
                selectedModelData={selectedModelData}
                isExpanded={isExpanded}
                setIsExpanded={setIsExpanded}
            />

            <ModelSelectionCollapsible
                models={models}
                selectedModelData={selectedModelData}
                isExpanded={isExpanded}
            />
        </Card>
    );
};

export default ModelSelection;
