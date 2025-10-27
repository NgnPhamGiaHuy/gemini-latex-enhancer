import React, { memo, useMemo } from "react";
import { cn } from "@/libs/utils";
import { Check } from "lucide-react";

interface StepMeta {
    id: string;
    title: string;
    description: string;
}

interface StepIndicatorProps {
    steps: readonly StepMeta[];
    currentStep: string;
    className?: string;
}

const StepIndicator: React.FC<StepIndicatorProps> = memo(
    ({ steps, currentStep, className }) => {
        const currentIndex = useMemo(
            () => steps.findIndex((step) => step.id === currentStep),
            [steps, currentStep]
        );

        const safeIndex = currentIndex >= 0 ? currentIndex : 0;

        return (
            <div className={cn("w-full", className)}>
                {/* ---------- Desktop Layout ---------- */}
                <div className="hidden sm:flex items-center justify-between">
                    {steps.map((step, index) => {
                        const isCompleted = index < safeIndex;
                        const isCurrent = step.id === currentStep;
                        const isUpcoming = index > safeIndex;

                        return (
                            <div key={step.id} className="flex items-center">
                                <div className="flex flex-col items-center">
                                    <div
                                        className={cn(
                                            "size-12 flex items-center justify-center bg-white nb-border nb-shadow",
                                            {
                                                "bg-accent text-accent-foreground":
                                                    isCompleted || isCurrent,
                                            }
                                        )}
                                        aria-label={`Step ${index + 1}: ${step.title}`}
                                    >
                                        {isCompleted ? (
                                            <Check className="size-5" />
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
                                                        isCurrent ||
                                                        isCompleted,
                                                    "text-mute-foreground":
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
                                        className={cn(
                                            "w-16 h-2 mx-4 nb-border",
                                            {
                                                "bg-accent": index < safeIndex,
                                                "bg-muted": index >= safeIndex,
                                            }
                                        )}
                                        aria-hidden="true"
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* ---------- Mobile Layout ---------- */}
                <div className="sm:hidden">
                    {steps.map((step, index) => {
                        const isCompleted = index < safeIndex;
                        const isCurrent = step.id === currentStep;

                        return (
                            <div key={step.id} className="flex items-center">
                                <div
                                    className={cn(
                                        "size-10 flex items-center justify-center nb-border nb-shadow bg-white",
                                        {
                                            "bg-accent text-accent-foreground":
                                                isCompleted || isCurrent,
                                        }
                                    )}
                                    aria-label={`Step ${index + 1}: ${step.title}`}
                                >
                                    {isCompleted ? (
                                        <Check className="size-4" />
                                    ) : (
                                        <span className="text-sm font-bold">
                                            {index + 1}
                                        </span>
                                    )}
                                </div>
                                {index < steps.length - 1 && (
                                    <div
                                        className={cn(
                                            "w-8 h-2 mx-2 nb-border",
                                            {
                                                "bg-accent": index < safeIndex,
                                                "bg-muted": index >= safeIndex,
                                            }
                                        )}
                                        aria-hidden="true"
                                    />
                                )}
                            </div>
                        );
                    })}

                    {/* Current Step Info */}
                    <div className="text-center">
                        <p className="text-sm sm:text-base text-foreground font-bold uppercase">
                            {steps[safeIndex]?.title}
                        </p>
                        <p className="text-xs sm:text-sm text-muted-foreground">
                            {steps[safeIndex]?.description}
                        </p>
                    </div>
                </div>
            </div>
        );
    }
);

StepIndicator.displayName = "StepIndicator";

export default StepIndicator;
