import type { AIModel } from "@/libs/api";
import { MODEL_PATTERNS } from "@/constants";

export const getModelBadgeVariant = (model: AIModel): string => {
    if (model.default) return MODEL_PATTERNS.badge.default;

    for (const [pattern, variant] of Object.entries(MODEL_PATTERNS.badge)) {
        if (model.id.includes(pattern)) return variant;
    }

    return "secondary";
};

export const getModelDescription = (model: AIModel): string => {
    const baseDesc = model.description || "No description available";

    for (const [pattern, suffix] of Object.entries(
        MODEL_PATTERNS.description
    )) {
        if (model.id.includes(pattern)) {
            return `${baseDesc} (${suffix})`;
        }
    }
    return baseDesc;
};

export const getModelCategory = (model: AIModel): string => {
    for (const [pattern, category] of Object.entries(MODEL_PATTERNS.category)) {
        if (model.id.includes(pattern)) return category;
    }
    return "Other";
};
