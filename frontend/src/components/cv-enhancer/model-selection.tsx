"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, Loader2, AlertCircle, Search, ChevronDown, Settings } from "lucide-react";

import type { AIModel } from "@/lib/api";
import type { ModelSelectionProps } from "@/types";

import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue, SelectGroup, SelectLabel } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";

const ModelSelection = ({ models, selectedModel, defaultModel, isLoading, error, onModelChange, className }: ModelSelectionProps) => {
    const [searchTerm, setSearchTerm] = useState("");
    const [isExpanded, setIsExpanded] = useState(false);

    const getModelBadgeVariant = (model: AIModel) => {
        if (model.default) return "default";
        if (model.id.includes("pro")) return "secondary";
        if (model.id.includes("preview") || model.id.includes("exp")) return "outline";
        return "secondary";
    };

    const getModelDescription = (model: AIModel) => {
        const baseDesc = model.description || "No description available";

        if (model.id.includes("preview")) {
            return `${baseDesc} (Preview)`;
        }
        if (model.id.includes("exp")) {
            return `${baseDesc} (Experimental)`;
        }
        if (model.id.includes("lite")) {
            return `${baseDesc} (Lightweight)`;
        }
        if (model.id.includes("pro")) {
            return `${baseDesc} (Advanced)`;
        }

        return baseDesc;
    };

    const getModelCategory = (model: AIModel) => {
        if (model.id.includes("2.5")) return "2.5 Series";
        if (model.id.includes("2.0")) return "2.0 Series";
        if (model.id.includes("1.5")) return "1.5 Series";
        if (model.id.includes("1.0")) return "1.0 Series";
        if (model.id.includes("gemma")) return "Gemma Series";
        return "Other";
    };

    // Filter and group models
    const filteredAndGroupedModels = useMemo(() => {
        const filtered = models.filter((model) => model.name.toLowerCase().includes(searchTerm.toLowerCase()) || model.id.toLowerCase().includes(searchTerm.toLowerCase()) || model.description.toLowerCase().includes(searchTerm.toLowerCase()));

        const grouped = filtered.reduce(
            (acc, model) => {
                const category = getModelCategory(model);
                if (!acc[category]) acc[category] = [];
                acc[category].push(model);
                return acc;
            },
            {} as Record<string, AIModel[]>
        );

        // Sort categories by preference
        const categoryOrder = ["2.5 Series", "2.0 Series", "1.5 Series", "1.0 Series", "Gemma Series", "Other"];
        const sortedCategories = categoryOrder.filter((cat) => grouped[cat]?.length > 0);

        return { grouped, sortedCategories };
    }, [models, searchTerm]);

    const selectedModelData = models.find((m) => m.id === selectedModel);

    if (error) {
        return (
            <Card className={cn("transition-all duration-300", className)}>
                <CardHeader className="pb-3">
                    <CardTitle className="flex items-center gap-2 text-lg">
                        <Brain className="h-5 w-5 text-primary" />
                        AI Model Selection
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>Failed to load available models. Using default model: {defaultModel}</AlertDescription>
                    </Alert>
                </CardContent>
            </Card>
        );
    }

    if (isLoading) {
        return (
            <Card className={cn("transition-all duration-300", className)}>
                <CardHeader className="pb-3">
                    <CardTitle className="flex items-center gap-2 text-lg">
                        <Brain className="h-5 w-5 text-primary" />
                        AI Model Selection
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center justify-center py-8">
                        <Loader2 className="h-6 w-6 animate-spin text-primary" />
                        <span className="ml-2 text-muted-foreground">Loading AI models...</span>
                    </div>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className={cn("transition-all duration-300 hover:shadow-md", isExpanded && "shadow-lg", className)}>
            {/* Header - Always Visible */}
            <CardHeader className="pb-3 cursor-pointer select-none" onClick={() => setIsExpanded(!isExpanded)}>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Settings className="h-5 w-5 text-primary" />
                        <CardTitle className="text-lg">AI Model</CardTitle>
                        <Badge variant="outline" className="text-xs">
                            {selectedModelData?.name || "Default"}
                        </Badge>
                    </div>
                    <motion.div animate={{ rotate: isExpanded ? 180 : 0 }} transition={{ duration: 0.2, ease: "easeInOut" }}>
                        <ChevronDown className="h-5 w-5 text-muted-foreground" />
                    </motion.div>
                </div>

                {/* Selected Model Summary */}
                <div className="text-sm text-muted-foreground">{selectedModelData ? <span>{selectedModelData.description}</span> : <span>Choose from {models.length} available AI models</span>}</div>
            </CardHeader>

            {/* Collapsible Content */}
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
                            {/* Search Input */}
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                <Input placeholder="Search models..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="pl-10" />
                            </div>

                            {/* Model Selection */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Choose AI Model</label>
                                <Select value={selectedModel} onValueChange={onModelChange}>
                                    <SelectTrigger className="h-11">
                                        <SelectValue placeholder="Select a model">
                                            <div className="flex items-center gap-2">
                                                <span>{selectedModelData?.name || "Select a model"}</span>
                                                {selectedModelData?.default && (
                                                    <Badge variant="default" className="text-xs">
                                                        Default
                                                    </Badge>
                                                )}
                                            </div>
                                        </SelectValue>
                                    </SelectTrigger>
                                    <SelectContent className="max-h-96">
                                        {filteredAndGroupedModels.sortedCategories.map((category) => (
                                            <SelectGroup key={category}>
                                                <SelectLabel className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                                                    {category} ({filteredAndGroupedModels.grouped[category].length})
                                                </SelectLabel>
                                                {filteredAndGroupedModels.grouped[category].map((model) => (
                                                    <SelectItem key={model.id} value={model.id}>
                                                        <div className="flex items-center justify-between w-full">
                                                            <div className="flex flex-col items-start">
                                                                <div className="flex items-center gap-2">
                                                                    <span className="font-medium">{model.name}</span>
                                                                    {model.default && (
                                                                        <Badge variant="default" className="text-xs">
                                                                            Default
                                                                        </Badge>
                                                                    )}
                                                                    <Badge variant={getModelBadgeVariant(model)} className="text-xs">
                                                                        {model.id.includes("pro") ? "Pro" : model.id.includes("preview") ? "Preview" : model.id.includes("exp") ? "Exp" : model.id.includes("lite") ? "Lite" : "Standard"}
                                                                    </Badge>
                                                                </div>
                                                                <span className="text-xs text-muted-foreground">{getModelDescription(model)}</span>
                                                            </div>
                                                        </div>
                                                    </SelectItem>
                                                ))}
                                            </SelectGroup>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            {/* Selected Model Info */}
                            {selectedModelData && (
                                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="p-3 bg-muted/50 rounded-lg border">
                                    <div className="text-sm">
                                        <div className="font-medium mb-1 flex items-center gap-2">
                                            <Brain className="h-4 w-4 text-primary" />
                                            {selectedModelData.name}
                                        </div>
                                        <div className="text-muted-foreground">{selectedModelData.description}</div>
                                    </div>
                                </motion.div>
                            )}

                            {/* Help Text */}
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="text-xs text-muted-foreground bg-blue-50 dark:bg-blue-950/20 p-3 rounded-lg border border-blue-200 dark:border-blue-800">
                                💡 Different models may provide varying quality and speed. Pro models typically offer better results but may take longer to process.
                            </motion.div>
                        </CardContent>
                    </motion.div>
                )}
            </AnimatePresence>
        </Card>
    );
};

export default ModelSelection;
