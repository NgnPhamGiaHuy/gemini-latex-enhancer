"use client";

import { useMemo } from "react";

import type { AIModel } from "@/libs/api";

import { useAppSelector, useAppDispatch } from "@/store/hooks";
import { setSelectedModel } from "@/store/slices/modelSelectionSlice";
import { getModelBadgeVariant, getModelCategory, getModelDescription, } from "@/utils";

import { Badge } from "@/components/ui/Badge";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue, } from "@/components/ui/Select";

interface ModelSelectDropdownProps {
    models: AIModel[];
    searchTerm: string;
}

const ModelSelectDropdown = ({
    models,
    searchTerm,
}: ModelSelectDropdownProps) => {
    const dispatch = useAppDispatch();
    const selectedModel = useAppSelector(
        (state) => state.modelSelection.selectedModel
    );

    const selectedModelData = models.find((m) => m.id === selectedModel);

    const handleModelChange = (modelId: string) => {
        dispatch(setSelectedModel(modelId));
    };

    const filteredAndGroupedModels = useMemo(() => {
        const filtered = models.filter(
            (model) =>
                model.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                model.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                model.description
                    .toLowerCase()
                    .includes(searchTerm.toLowerCase())
        );

        const grouped = filtered.reduce(
            (acc, model) => {
                const category = getModelCategory(model);

                if (!acc[category]) acc[category] = [];

                acc[category].push(model);

                return acc;
            },
            {} as Record<string, AIModel[]>
        );

        const categoryOrder = [
            "2.5 Series",
            "2.0 Series",
            "1.5 Series",
            "1.0 Series",
            "Gemma Series",
            "Other",
        ];

        const sortedCategories = categoryOrder.filter(
            (cat) => grouped[cat]?.length > 0
        );

        return { grouped, sortedCategories };
    }, [models, searchTerm]);

    return (
        <div className="space-y-2">
            <label className="text-sm font-medium">Choose AI Model</label>
            <Select value={selectedModel} onValueChange={handleModelChange}>
                <SelectTrigger className="h-11">
                    <SelectValue placeholder="Select a model">
                        <div className="flex items-center gap-2">
                            <span>
                                {selectedModelData?.name || "Select a model"}
                            </span>
                            {selectedModelData?.default && (
                                <Badge variant="default" className="text-xs">
                                    Default
                                </Badge>
                            )}
                        </div>
                    </SelectValue>
                </SelectTrigger>
                <SelectContent className="max-h-96">
                    {filteredAndGroupedModels.sortedCategories.map(
                        (category) => (
                            <SelectGroup key={category}>
                                <SelectLabel className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                                    {category} (
                                    {
                                        filteredAndGroupedModels.grouped[
                                            category
                                        ].length
                                    }
                                    )
                                </SelectLabel>
                                {filteredAndGroupedModels.grouped[category].map(
                                    (model) => (
                                        <SelectItem
                                            key={model.id}
                                            value={model.id}
                                        >
                                            <div className="flex items-center justify-between w-full">
                                                <div className="flex flex-col items-start">
                                                    <div className="flex items-center gap-2">
                                                        <span className="font-medium">
                                                            {model.name}
                                                        </span>
                                                        {model.default && (
                                                            <Badge
                                                                variant="default"
                                                                className="text-xs"
                                                            >
                                                                Default
                                                            </Badge>
                                                        )}
                                                        <Badge
                                                            variant={
                                                                getModelBadgeVariant(
                                                                    model
                                                                ) as
                                                                    | "default"
                                                                    | "secondary"
                                                                    | "destructive"
                                                                    | "outline"
                                                            }
                                                            className="text-xs"
                                                        >
                                                            {model.id.includes(
                                                                "pro"
                                                            )
                                                                ? "Pro"
                                                                : model.id.includes(
                                                                        "preview"
                                                                    )
                                                                  ? "Preview"
                                                                  : model.id.includes(
                                                                          "exp"
                                                                      )
                                                                    ? "Exp"
                                                                    : model.id.includes(
                                                                            "lite"
                                                                        )
                                                                      ? "Lite"
                                                                      : "Standard"}
                                                        </Badge>
                                                    </div>
                                                    <span className="text-xs text-muted-foreground">
                                                        {getModelDescription(
                                                            model
                                                        )}
                                                    </span>
                                                </div>
                                            </div>
                                        </SelectItem>
                                    )
                                )}
                            </SelectGroup>
                        )
                    )}
                </SelectContent>
            </Select>
        </div>
    );
};

export default ModelSelectDropdown;
