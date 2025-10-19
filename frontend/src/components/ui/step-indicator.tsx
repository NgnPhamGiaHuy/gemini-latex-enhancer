"use client";

import { cn } from "@/lib/utils";
import { Check } from "lucide-react";
import type { StepIndicatorProps } from "@/types";

export const StepIndicator = ({
    steps,
    currentStep,
    className,
}: StepIndicatorProps) => {
    const currentIndex = steps.findIndex((step) => step.id === currentStep);

    return (
        <div className={cn("w-full", className)}>
            {/* Desktop Layout */}
            <div className="hidden sm:flex items-center justify-between">
                {steps.map((step, index) => {
                    const isCompleted = index < currentIndex;
                    const isCurrent = step.id === currentStep;
                    const isUpcoming = index > currentIndex;

                    return (
                        <div key={step.id} className="flex items-center">
                            <div className="flex flex-col items-center">
                                <div
                                    className={cn(
                                        "flex h-12 w-12 items-center justify-center nb-border nb-shadow bg-white",
                                        {
                                            "bg-accent text-accent-foreground":
                                                isCompleted || isCurrent,
                                        }
                                    )}
                                    aria-label={`Step ${index + 1}: ${step.title}`}
                                >
                                    {isCompleted ? (
                                        <Check className="h-5 w-5" />
                                    ) : (
                                        <span className="text-sm sm:text-base font-bold">
                                            {index + 1}
                                        </span>
                                    )}
                                </div>
                                <div className="mt-2 text-center">
                                    <p
                                        className={cn(
                                            "text-sm sm:text-base font-bold uppercase",
                                            {
                                                "text-foreground":
                                                    isCurrent || isCompleted,
                                                "text-muted-foreground":
                                                    isUpcoming,
                                            }
                                        )}
                                    >
                                        {step.title}
                                    </p>
                                    <p className="text-xs sm:text-sm text-muted-foreground">
                                        {step.description}
                                    </p>
                                </div>
                            </div>
                            {index < steps.length - 1 && (
                                <div
                                    className={cn("mx-4 h-2 w-16 nb-border", {
                                        "bg-accent": index < currentIndex,
                                        "bg-muted": index >= currentIndex,
                                    })}
                                    aria-hidden="true"
                                />
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Mobile Layout */}
            <div className="sm:hidden">
                <div className="flex items-center justify-between mb-4">
                    {steps.map((step, index) => {
                        const isCompleted = index < currentIndex;
                        const isCurrent = step.id === currentStep;
                        const isUpcoming = index > currentIndex;

                        return (
                            <div key={step.id} className="flex items-center">
                                <div
                                    className={cn(
                                        "flex h-10 w-10 items-center justify-center nb-border nb-shadow bg-white",
                                        {
                                            "bg-accent text-accent-foreground":
                                                isCompleted || isCurrent,
                                        }
                                    )}
                                    aria-label={`Step ${index + 1}: ${step.title}`}
                                >
                                    {isCompleted ? (
                                        <Check className="h-4 w-4" />
                                    ) : (
                                        <span className="text-sm font-bold">
                                            {index + 1}
                                        </span>
                                    )}
                                </div>
                                {index < steps.length - 1 && (
                                    <div
                                        className={cn(
                                            "mx-2 h-2 w-8 nb-border",
                                            {
                                                "bg-accent":
                                                    index < currentIndex,
                                                "bg-muted":
                                                    index >= currentIndex,
                                            }
                                        )}
                                        aria-hidden="true"
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* Current Step Info */}
                <div className="text-center">
                    <p className="text-sm sm:text-base font-bold uppercase text-foreground">
                        {steps[currentIndex]?.title}
                    </p>
                    <p className="text-xs sm:text-sm text-muted-foreground">
                        {steps[currentIndex]?.description}
                    </p>
                </div>
            </div>
        </div>
    );
};
